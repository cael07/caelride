from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.orm import Session
import sqlalchemy as sa
import json
from typing import Dict, List, Optional
from ..database import get_db
from ..auth.models import Booking, User
from ..auth.service import get_user_by_id
from pydantic import BaseModel

router = APIRouter(prefix="/ride", tags=["Ride"])

# Connection Manager for WebSockets
class ConnectionManager:
    def __init__(self):
        # List of active connections: [(user_id, WebSocket)]
        self.active_connections: List[tuple] = []

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections.append((user_id, websocket))
        print(f"[WS MANAGER] User {user_id} connected. Total active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket, user_id: int):
        self.active_connections = [conn for conn in self.active_connections if conn[1] != websocket]
        print(f"[WS MANAGER] Connection for user {user_id} removed. Remaining connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, user_id: int):
        print(f"[WS MANAGER] Trying to send personal message to User {user_id}...")
        targets = [ws for uid, ws in self.active_connections if uid == user_id]
        if targets:
            for ws in targets:
                try:
                    await ws.send_text(message)
                except Exception as e:
                    print(f"[WS MANAGER] Failed to send to a socket: {e}")
            print(f"[WS MANAGER] Successfully sent message to User {user_id} ({len(targets)} sockets).")
        else:
            print(f"[WS MANAGER] FAILED to send: User {user_id} is NOT connected.")

    async def broadcast(self, message: str):
        print(f"[WS MANAGER] Broadcasting message to {len(self.active_connections)} active connections...")
        dead_connections = []
        for uid, connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"[WS MANAGER] Broadcast failed to connection for user {uid}: {e}")
                dead_connections.append((uid, connection))
                
        for dead in dead_connections:
            if dead in self.active_connections:
                self.active_connections.remove(dead)

manager = ConnectionManager()

class BookingCreate(BaseModel):
    passenger_id: int
    pickup_lat: float
    pickup_lng: float
    dropoff_lat: float
    dropoff_lng: float
    pickup_address: Optional[str] = None
    dropoff_address: Optional[str] = None
    document_image: Optional[str] = None
    document_info: Optional[str] = None
    document_tip: Optional[str] = None

@router.get("/active/{user_id}")
async def get_active_booking(user_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(
        sa.or_(
            Booking.passenger_id == user_id,
            Booking.driver_id == user_id
        ),
        Booking.status.in_(["pending", "accepted", "arrived", "started"])
    ).order_by(Booking.id.desc()).first()
    
    if not booking:
        return None
        
    passenger = get_user_by_id(db, booking.passenger_id)
    driver = get_user_by_id(db, booking.driver_id) if booking.driver_id else None
    
    return {
        "id": booking.id,
        "passenger_id": booking.passenger_id,
        "passenger_name": passenger.full_name if passenger else "Passenger",
        "passenger_phone": getattr(passenger, "phone_number", None) or getattr(passenger, "username", "09170000000"),
        "passenger_image": getattr(passenger, "face_image_base64", None),
        "driver_id": booking.driver_id,
        "driver_name": driver.full_name if driver else None,
        "driver_phone": (getattr(driver, "phone_number", None) or getattr(driver, "username", "09170000001")) if driver else None,
        "driver_image": getattr(driver, "face_image_base64", None),
        "driver_license_number": getattr(driver, "license_number", None),
        "driver_plate_number": getattr(driver, "cr_plate_number", None),
        "driver_moto_brand": getattr(driver, "cr_brand", None),
        "driver_moto_model": getattr(driver, "cr_model", None),
        "pickup_lat": booking.pickup_lat,
        "pickup_lng": booking.pickup_lng,
        "dropoff_lat": booking.dropoff_lat,
        "dropoff_lng": booking.dropoff_lng,
        "status": booking.status,
        "document_image": booking.document_image,
        "document_info": booking.document_info,
        "document_tip": booking.document_tip
    }

@router.post("/bookings")
async def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    # Check for existing active booking first
    active = db.query(Booking).filter(
        Booking.passenger_id == booking.passenger_id,
        Booking.status.in_(["pending", "accepted", "arrived", "started"])
    ).first()
    
    if active:
        return {"message": "Active booking exists", "booking_id": active.id, "already_exists": True}

    # Haversine distance calculation in km to match the passenger app exactly
    import math
    
    lat1, lon1 = booking.pickup_lat, booking.pickup_lng
    lat2, lon2 = booking.dropoff_lat, booking.dropoff_lng
    
    R = 6371.0  # Earth's radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    
    a = math.sin(d_lat / 2.0)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    dist = R * c
    
    # Matching passenger calculation exactly (Minimum fare 50 PHP, dist * 15.2)
    calculated_fare = float(max(50, round(dist * 15.2)))

    new_booking = Booking(
        passenger_id=booking.passenger_id,
        pickup_lat=booking.pickup_lat,
        pickup_lng=booking.pickup_lng,
        dropoff_lat=booking.dropoff_lat,
        dropoff_lng=booking.dropoff_lng,
        pickup_address=booking.pickup_address,
        dropoff_address=booking.dropoff_address,
        amount=calculated_fare,
        status="pending",
        document_image=booking.document_image,
        document_info=booking.document_info,
        document_tip=booking.document_tip
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    # Broadcast to all drivers that a new booking is available
    passenger = get_user_by_id(db, new_booking.passenger_id)
    await manager.broadcast(json.dumps({
        "type": "new_booking",
        "booking": {
            "id": new_booking.id,
            "passenger_id": new_booking.passenger_id,
            "passenger_name": passenger.full_name if passenger else "Passenger",
            "passenger_image": getattr(passenger, "face_image_base64", None),
            "pickup_lat": new_booking.pickup_lat,
            "pickup_lng": new_booking.pickup_lng,
            "dropoff_lat": new_booking.dropoff_lat,
            "dropoff_lng": new_booking.dropoff_lng,
            "pickup_address": new_booking.pickup_address,
            "dropoff_address": new_booking.dropoff_address,
            "amount": new_booking.amount,
            "status": new_booking.status,
            "document_image": new_booking.document_image,
            "document_info": new_booking.document_info,
            "document_tip": new_booking.document_tip
        }
    }))
    
    return {"message": "Booking created successfully", "booking_id": new_booking.id, "amount": new_booking.amount}

@router.get("/bookings")
async def get_bookings(db: Session = Depends(get_db)):
    bookings = db.query(Booking).filter(Booking.status == "pending").all()
    results = []
    for b in bookings:
        passenger = get_user_by_id(db, b.passenger_id)
        results.append({
            "id": b.id,
            "passenger_id": b.passenger_id,
            "passenger_name": passenger.full_name if passenger else "Passenger",
            "passenger_image": getattr(passenger, "face_image_base64", None),
            "pickup_lat": b.pickup_lat,
            "pickup_lng": b.pickup_lng,
            "dropoff_lat": b.dropoff_lat,
            "dropoff_lng": b.dropoff_lng,
            "pickup_address": b.pickup_address,
            "dropoff_address": b.dropoff_address,
            "amount": b.amount,
            "status": b.status,
            "document_image": b.document_image,
            "document_info": b.document_info,
            "document_tip": b.document_tip
        })
    return results

class AcceptBooking(BaseModel):
    driver_id: int

@router.post("/bookings/{booking_id}/accept")
async def accept_booking(booking_id: int, request: AcceptBooking, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.status != "pending":
        raise HTTPException(status_code=400, detail=f"Ride is already {booking.status}")

    driver = get_user_by_id(db, request.driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
        
    fare = booking.amount or 0.0
    required_balance = round(fare * 0.3, 2)
    driver_balance = driver.balance or 0.0
    
    if driver_balance < required_balance:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient balance. You need at least PHP {required_balance:.2f} (30% of fare PHP {fare:.2f}) to accept this booking. Current balance: PHP {driver_balance:.2f}."
        )
        
    # Atomically claim the booking by transitioning status from pending -> accepted.
    # This executes a single atomic SQL UPDATE query with status check inside WHERE filter:
    # UPDATE ride_bookings SET driver_id = X, status = 'accepted' WHERE id = Y AND status = 'pending'
    # SQL database engines queue updates sequentially, guaranteeing only one driver succeeds.
    updated_rows = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.status == "pending"
    ).update({
        "driver_id": request.driver_id,
        "status": "accepted"
    })

    if updated_rows == 0:
        raise HTTPException(
            status_code=400,
            detail="This ride has already been accepted by another driver."
        )

    # Safely deduct 30% of the fare from the claiming driver's balance
    driver.balance = round(driver_balance - required_balance, 2)
    
    # Log the balance deduction
    from ..auth.models import BalanceLog
    log_entry = BalanceLog(
        user_id=driver.id,
        created_by_id=driver.id,
        amount=-required_balance,
        new_balance=driver.balance
    )
    db.add(log_entry)
    db.commit()
    
    # Notify passenger that ride was accepted
    accept_msg = json.dumps({
        "type": "ride_accepted",
        "booking_id": booking.id,
        "driver_id": request.driver_id,
        "driver_name": driver.full_name if driver else "Driver",
        "driver_phone": getattr(driver, "phone_number", None) or getattr(driver, "username", "09170000001"),
        "driver_image": getattr(driver, "face_image_base64", None),
        "driver_license_number": getattr(driver, "license_number", None),
        "driver_plate_number": getattr(driver, "cr_plate_number", None),
        "driver_moto_brand": getattr(driver, "cr_brand", None),
        "driver_moto_model": getattr(driver, "cr_model", None)
    })
    await manager.send_personal_message(accept_msg, booking.passenger_id)
    
    # Notify all other drivers to remove this from their list
    await manager.broadcast(json.dumps({
        "type": "booking_taken",
        "booking_id": booking.id
    }))
    
    passenger = get_user_by_id(db, booking.passenger_id)
    return {
        "message": "Booking accepted",
        "booking": {
            "id": booking.id,
            "passenger_id": booking.passenger_id,
            "passenger_name": passenger.full_name if passenger else "Passenger",
            "passenger_phone": getattr(passenger, "phone_number", None) or getattr(passenger, "username", "09170000000"),
            "passenger_image": getattr(passenger, "face_image_base64", None),
            "driver_id": booking.driver_id,
            "driver_name": driver.full_name if driver else "Driver",
            "driver_phone": getattr(driver, "phone_number", None) or getattr(driver, "username", "09170000001"),
            "driver_image": getattr(driver, "face_image_base64", None),
            "pickup_lat": booking.pickup_lat,
            "pickup_lng": booking.pickup_lng,
            "dropoff_lat": booking.dropoff_lat,
            "dropoff_lng": booking.dropoff_lng,
            "status": booking.status,
            "document_image": booking.document_image,
            "document_info": booking.document_info,
            "document_tip": booking.document_tip
        }
    }

@router.post("/bookings/{booking_id}/arrived")
async def notify_arrived(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.status = "arrived"
    db.commit()
    
    # Notify passenger
    msg = json.dumps({
        "type": "ride_arrived",
        "booking_id": booking.id
    })
    await manager.send_personal_message(msg, booking.passenger_id)
    
    # Notify driver too so their UI updates
    if booking.driver_id:
        await manager.send_personal_message(msg, booking.driver_id)
        
    return {"message": "Arrival notification sent to all parties"}

@router.post("/bookings/{booking_id}/start")
async def start_ride(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.status = "started"
    db.commit()
    
    # Notify parties
    msg = json.dumps({
        "type": "ride_started",
        "booking_id": booking.id
    })
    await manager.send_personal_message(msg, booking.passenger_id)
    
    # Notify driver
    if booking.driver_id:
        await manager.send_personal_message(msg, booking.driver_id)
        
    return {"message": "Ride started"}

class CompleteRideRequest(BaseModel):
    received_image: Optional[str] = None
    signature_image: Optional[str] = None

@router.post("/bookings/{booking_id}/complete")
async def complete_ride(booking_id: int, request: Optional[CompleteRideRequest] = None, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.status = "completed"
    if request:
        if request.received_image:
            booking.received_image = request.received_image
        if request.signature_image:
            booking.signature_image = request.signature_image

    db.commit()
    
    # Notify parties
    msg = json.dumps({
        "type": "ride_completed",
        "booking_id": booking.id
    })
    await manager.send_personal_message(msg, booking.passenger_id)

    # Notify driver
    if booking.driver_id:
        await manager.send_personal_message(msg, booking.driver_id)
        
    return {"message": "Ride completed"}

@router.post("/bookings/{booking_id}/cancel")
async def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # If the ride is cancelled after driver acceptance, refund the 30% fee to the driver
    if booking.driver_id and booking.status in ("accepted", "arrived"):
        refund_amount = round((booking.amount or 0.0) * 0.3, 2)
        driver = get_user_by_id(db, booking.driver_id)
        if driver:
            driver.balance = round((driver.balance or 0.0) + refund_amount, 2)
            # Log the balance refund
            from ..auth.models import BalanceLog
            log_entry = BalanceLog(
                user_id=driver.id,
                created_by_id=driver.id,
                amount=refund_amount,
                new_balance=driver.balance
            )
            db.add(log_entry)
            print(f"[CANCEL BOOKING] Refunded PHP {refund_amount} to Driver {driver.id}. New balance: PHP {driver.balance}")

    booking.status = "cancelled"
    db.commit()
    
    # Notify everyone that this ride is cancelled
    cancel_msg = json.dumps({
        "type": "ride_cancelled",
        "booking_id": booking.id
    })
    
    # Broadcast to all connected users (drivers and passengers)
    # This ensures all drivers remove it from their "Incoming Requests" list
    await manager.broadcast(cancel_msg)
        
    return {"message": "Booking cancelled"}

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            print(f"[WS RECEIVE] From User {user_id}: {message}")
            
            if message.get("type") == "location_update":
                # Driver is updating their location
                booking_id = message.get("booking_id")
                passenger_id = message.get("passenger_id")
                lat = message.get("lat")
                lng = message.get("lng")
                
                # Send to the specific passenger
                await manager.send_personal_message(json.dumps({
                    "type": "driver_location",
                    "lat": lat,
                    "lng": lng,
                    "booking_id": booking_id
                }), passenger_id)

            elif message.get("type") in ("chat_message", "call_offer", "call_answer", "call_ice", "call_end"):
                # Relay chat and WebRTC signaling messages to the target user.
                # The backend acts purely as a relay — it does not process audio or store chat.
                target_user_id = message.get("target_user_id")
                if target_user_id:
                    # Forward the full message payload (including sender_id, text, sdp, candidate, etc.)
                    await manager.send_personal_message(json.dumps(message), int(target_user_id))
                else:
                    print(f"[WS RELAY ERROR] Message type {message.get('type')} missing target_user_id")
                
    except Exception:
        manager.disconnect(websocket, user_id)
