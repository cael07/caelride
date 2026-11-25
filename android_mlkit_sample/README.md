Android ML Kit CR OCR sample (on-device)
======================================

This folder contains a minimal Kotlin example showing how to run Google ML Kit on-device
Text Recognition and parse a Philippine Certificate of Registration (CR) fields: plate,
brand, color, year and owner name. It's intended as a drop-in snippet you can add to an
existing Android app (no Google Cloud billing required).

Key points
- Uses ML Kit on-device Text Recognition (free)
- Parses raw OCR text with heuristic rules (ported from web parsing logic)
- Call `TextParser.parseCR(rawText)` to get structured fields

Integration
1. Add ML Kit dependency in your module `build.gradle`:

```gradle
dependencies {
    implementation 'com.google.mlkit:text-recognition:16.1.0'
}
```

2. Add an Activity that captures or selects an image and passes a `Bitmap` to `runTextRecognition(bitmap)`.
3. Use the `TextParser` helper to extract CR fields and then send them to your backend or UI.

Files
- `MainActivity.kt` — minimal example to run ML Kit on a bitmap and call the parser
- `TextParser.kt` — parser that extracts CR fields from OCR'd text

Notes
- This is a sample helper; tune the heuristics for your documents and OCR quality.
- The web frontend already uses Tesseract.js; this lets you test on web and later reuse parsing logic on Android.
