import re
import difflib
from typing import Dict

KNOWN_BRANDS = ['HONDA', 'YAMAHA', 'SUZUKI', 'KAWASAKI', 'TOYOTA', 'NISSAN', 'ISUZU', 'MITSUBISHI', 'MAZDA', 'HYUNDAI', 'KIA', 'FORD', 'CHEVROLET', 'HINO']
KNOWN_COLORS = ['BLACK', 'WHITE', 'RED', 'BLUE', 'GREEN', 'YELLOW', 'BROWN', 'SILVER', 'GRAY', 'GREY', 'ORANGE', 'GOLD', 'MAROON', 'BEIGE']

GENERIC_TOKENS = re.compile(r"(VEHICLE|MOTOR|TYPE|CATEGORY|WITHOUT|SIDE|CAR|FUEL|ENGINE|CHASSIS|FILE|MODEL|YEAR|MAKE|BRAND|OWNER|REGISTERED|CERTIFICATE|REGISTRATION|OFFICIAL|DEPARTMENT|TRANSPORTATION)", re.I)


def _extract_field(lines_raw, labels, reject_generic=False):
    """Extract a field value by finding the label and getting the value after it or on next lines."""
    upper_lines = [l.upper() for l in lines_raw]
    up_labels = [l.upper() for l in labels]
    
    for i, upper in enumerate(upper_lines):
        for label in up_labels:
            idx = upper.find(label)
            if idx != -1:
                # Get value after label on same line
                value = lines_raw[i][idx + len(label):].strip()
                value = re.sub(r'^[:\-.\s#]+', '', value).strip()
                
                # Limit to first few words to avoid capturing next field
                if value:
                    words = value.split()
                    # Only take first 4 words to avoid multi-field contamination
                    value = ' '.join(words[:4]).strip()
                    value = re.sub(r'^[:\-.\s#]+', '', value).strip()
                
                if value and not any(lbl in value.upper() for lbl in up_labels):
                    if not reject_generic or not GENERIC_TOKENS.search(value):
                        return value
                
                # check next line for continuation
                if i + 1 < len(lines_raw):
                    nxt = lines_raw[i + 1].strip()
                    if nxt and not any(lbl in nxt.upper() for lbl in up_labels):
                        # skip if next line looks like another labeled field
                        pre = nxt.split(':', 1)[0].strip().upper()
                        if pre and any(pre.startswith(tok) for tok in ('COLOR', 'YEAR', 'OWNER', 'PLATE', 'MODEL', 'ENGINE', 'CHASSIS', 'BODY', 'TYPE', 'SERIES', 'MAKE', 'BRAND', 'REGISTRATION')):
                            pass
                        else:
                            # Also limit continuation to avoid multi-field mixing
                            nxt_words = nxt.split()
                            nxt = ' '.join(nxt_words[:4]).strip()
                            if not reject_generic or not GENERIC_TOKENS.search(nxt):
                                return nxt
    return ''


def parse_cr_text(raw_text: str) -> Dict[str, str]:
    """Parse Certificate of Registration text and extract plate, brand, color, year, owner."""
    lines_raw = [l.strip() for l in raw_text.splitlines() if l.strip()]
    upper_lines = [l.upper() for l in lines_raw]
    raw_upper = raw_text.upper()

    # 1. Locate the PLATE NO. label line and sample its local window of lines
    plate_line_idx = -1
    for idx, l in enumerate(upper_lines):
        if 'PLATE' in l or 'REGISTRATION' in l:
            plate_line_idx = idx
            break
            
    # Collect words from context around PLATE label
    plate_context_words = []
    if plate_line_idx != -1:
        start = max(0, plate_line_idx - 1)
        end = min(len(lines_raw), plate_line_idx + 3)
        plate_context_words = []
        for i in range(start, end):
            # Split by common separators but preserve structure
            words = re.split(r'[\s:.\-#]+', lines_raw[i])
            plate_context_words.extend([w.strip() for w in words if w.strip()])

    plate = ''
    
    # Try to extract from immediate context first (most reliable)
    if plate_context_words:
        # Look for patterns like "R253EE", "NDG4819", etc in the context
        for word in plate_context_words:
            # Pattern checks
            word_upper = word.upper()
            # Match regional plates: R + 3 digits + 2 letters (e.g., R253EE)
            if re.match(r'^[A-Z]\d{3}[A-Z]{2}$', word_upper):
                plate = word_upper
                break
            # Match standard plates: 3 letters + 4 digits (e.g., NDG4819)
            if re.match(r'^[A-Z]{3}\d{4}$', word_upper):
                plate = word_upper
                break
            # Match motorcycle new format: 3 digits + 3-4 letters (e.g., 123ABC)
            if re.match(r'^\d{3}[A-Z]{3,4}$', word_upper):
                plate = word_upper
                break

    # Fallback: Use regex on a clean search area if word-by-word didn't work
    if not plate and plate_line_idx != -1:
        start = max(0, plate_line_idx - 1)
        end = min(len(lines_raw), plate_line_idx + 3)
        plate_search_text = ' '.join(lines_raw[start:end]).upper()
        clean_plate_search = re.sub(r'[^A-Z0-9\s]', ' ', plate_search_text)

        plate_patterns = [
            r'\b([A-Z]\d{3}[A-Z]{2})\b',          # Regional plates like R253EE
            r'\b([A-Z]{3}\d{4})\b',               # Standard car plates like NDG4819
            r'\b(\d{3}[A-Z]{3,4})\b',             # New motorcycle plates like 123ABC
            r'\b([A-Z]{2}\d{4,5})\b',             # Older motorcycle plates like MC12345
        ]

        for pat in plate_patterns:
            match = re.search(pat, clean_plate_search)
            if match:
                candidate = match.group(1)
                if candidate not in ['FOR', 'AND', 'THE', 'MVS', 'NEW', 'USE', 'GAS', 'LTO', 'MAX', 'MIN', 'NET']:
                    plate = candidate
                    break

    # Last resort fallback: search the whole text
    if not plate:
        whole_clean = re.sub(r'[^A-Z0-9\s]', ' ', raw_upper)
        plate_patterns = [
            r'\b([A-Z]\d{3}[A-Z]{2})\b',
            r'\b([A-Z]{3}\d{4})\b',
            r'\b(\d{3}[A-Z]{3,4})\b',
            r'\b([A-Z]{2}\d{4,5})\b',
        ]
        for pat in plate_patterns:
            match = re.search(pat, whole_clean)
            if match:
                candidate = match.group(1)
                if candidate not in ['FOR', 'AND', 'THE', 'MVS', 'NEW', 'USE', 'GAS', 'LTO', 'MAX', 'MIN', 'NET']:
                    plate = candidate
                    break

    # 2. Brand extraction (match KNOWN_BRANDS) - improved to avoid corruption
    brand = ''
    brand_line_idx = -1
    for idx, l in enumerate(upper_lines):
        if 'MAKE' in l or 'BRAND' in l:
            brand_line_idx = idx
            break

    # Search in local window for known brands first
    if brand_line_idx != -1:
        start = max(0, brand_line_idx)
        end = min(len(lines_raw), brand_line_idx + 2)
        brand_search_window = ' '.join(lines_raw[start:end]).upper()
        
        # Exact substring match for known brands
        for b in KNOWN_BRANDS:
            if b in brand_search_window:
                brand = b
                break

    # If not found in local window, try whole text
    if not brand:
        for b in KNOWN_BRANDS:
            if b in raw_upper:
                brand = b
                break

    # Last resort: extract and clean the field value
    if not brand:
        brand_raw = _extract_field(lines_raw, ['MAKE/BRAND', 'MAKE', 'BRAND'], False)
        brand_upper = brand_raw.upper()
        
        # Remove non-alphabetic characters
        brand_clean = re.sub(r'[^A-Z\s]', '', brand_upper).strip()
        
        # Try to find a known brand in the cleaned text
        for b in KNOWN_BRANDS:
            if b in brand_clean:
                brand = b
                break
        
        # If still not found, try close matching on first token
        if not brand and brand_clean:
            first_token = brand_clean.split()[0] if brand_clean.split() else ''
            if first_token and len(first_token) > 2:
                match = difflib.get_close_matches(first_token, KNOWN_BRANDS, n=1, cutoff=0.6)
                if match:
                    brand = match[0]

    def _extract_segment(flat_text: str, label_regex: re.Pattern, stop_regex: re.Pattern) -> str:
        m = label_regex.search(flat_text)
        if not m:
            return ''
        rest = flat_text[m.end():]
        stop = stop_regex.search(rest)
        return (rest[:stop.start()] if stop else rest).strip()

    flat = ' '.join(lines_raw).upper()

    # 3. Color extraction — match whole words near COLOR label only (avoid REGISTERED -> RED)
    color = ''
    color_line_idx = -1
    for idx, l in enumerate(upper_lines):
        # Accept both US and British spellings (COLOR / COLOUR)
        if re.search(r'\bCOLOU?R\b', l):
            color_line_idx = idx
            break

    color_context = ''
    if color_line_idx != -1:
        start = max(0, color_line_idx)
        end = min(len(lines_raw), color_line_idx + 5)
        color_context = ' '.join(lines_raw[start:end]).upper()
    color_seg = _extract_segment(
        flat,
        re.compile(r'\bCOLOU?R\b'),
        re.compile(r'\b(TYPE|FUEL|CLASSIFICATION|YEAR|OWNER|SERIES|BODY)\b'),
    )
    color_window = f'{color_context} {color_seg}'.strip()
    for c in KNOWN_COLORS:
        if re.search(rf'\b{re.escape(c)}\b', color_window):
            color = c
            break

    if not color and color_line_idx != -1:
        # Search a larger nearby window for the color value when it is positioned
        # below the label in a table column rather than immediately next line.
        for i in range(color_line_idx + 1, min(len(lines_raw), color_line_idx + 8)):
            color_word = re.sub(r'[^A-Z\s]', '', lines_raw[i].upper()).strip()
            if not color_word:
                continue
            for c in KNOWN_COLORS:
                if re.fullmatch(rf'\b{re.escape(c)}\b', color_word):
                    color = c
                    break
            if color:
                break

    if not color:
        color_raw = _extract_field(lines_raw, ['COLOR', 'COLOUR'], False)
        if color_raw:
            color_clean = re.sub(r'[^A-Z\s]', '', color_raw.upper()).strip()
            for word in color_clean.split():
                for c in KNOWN_COLORS:
                    if word == c:
                        color = c
                        break
                if color:
                    break
            # If still not found, accept a reasonable alphabetic token as fallback
            if not color:
                for word in color_clean.split():
                    w = re.sub(r'[^A-Z]', '', word)
                    if len(w) >= 3 and not GENERIC_TOKENS.search(w):
                        color = w
                        break

    # 4. Year extraction — prefer YEAR MODEL region; fix full-year regex in fallback
    year = ''
    year_re = re.compile(r'\b(?:19|20)\d{2}\b')

    year_line_idx = -1
    for idx, l in enumerate(upper_lines):
        if 'YEAR MODEL' in l or (re.search(r'\bYEAR\b', l) and re.search(r'\bMODEL\b', l)):
            year_line_idx = idx
            break
    if year_line_idx == -1:
        for idx, l in enumerate(upper_lines):
            if re.search(r'\bYEAR\b', l):
                year_line_idx = idx
                break

    year_window = ''
    if year_line_idx != -1:
        start = max(0, year_line_idx)
        end = min(len(lines_raw), year_line_idx + 4)
        year_window = ' '.join(lines_raw[start:end])
    year_seg = _extract_segment(
        flat,
        re.compile(r'\bYEAR\s*MODEL\b'),
        re.compile(r'\b(NEW|REBUILT|PISTON|OWNER|SERIES|BODY|ENCUMBERED)\b'),
    )
    year_search = f'{year_window} {year_seg}'.strip()
    year_matches = year_re.findall(year_search)
    if year_matches:
        year = max(year_matches, key=lambda y: int(y))

    if not year:
        all_years = [y for y in year_re.findall(raw_upper) if 1980 <= int(y) <= 2035]
        if all_years:
            year = max(all_years, key=lambda y: int(y))

    # 5. Owner's Name extraction (prioritizing OWNER labels)
    owner = ''
    for i, line in enumerate(upper_lines):
        if 'OWNER' in line:
            # Look at current line after the label
            line_val = re.sub(r'OWNER\'S NAME|OWNERS NAME|OWNER NAME|OWNER|[:\-#]', '', lines_raw[i], flags=re.I).strip()
            # Clean but preserve structure
            line_val = re.sub(r'[^A-Z\s\.,]', ' ', line_val.upper()).strip()
            line_val = re.sub(r'\s+', ' ', line_val).strip()
            
            if len(line_val) > 6 and len(line_val.split()) >= 2:
                owner = line_val
                break
            
            # If not on same line, check next few lines
            if not owner:
                for j in range(i + 1, min(i + 4, len(lines_raw))):
                    candidate = lines_raw[j].strip()
                    # Skip if it looks like a label or generic term
                    if not any(lbl in candidate.upper() for lbl in ['COLOR', 'YEAR', 'PLATE', 'BRAND', 'REGISTRATION', 'MAKE']):
                        candidate_clean = re.sub(r'[^A-Z\s\.,]', ' ', candidate.upper()).strip()
                        candidate_clean = re.sub(r'\s+', ' ', candidate_clean).strip()
                        if len(candidate_clean) > 6 and len(candidate_clean.split()) >= 2:
                            owner = candidate_clean
                            break
            if owner:
                break

    # Fallback: Look for multi-word names that aren't generic terms
    if not owner:
        for line in lines_raw:
            if not any(lbl in line.upper() for lbl in ['COLOR', 'YEAR', 'PLATE', 'BRAND', 'REGISTRATION', 'MAKE', 'CERTIFICATE', 'DEPARTMENT', 'MOTOR', 'VEHICLE']):
                candidate = re.sub(r'[^A-Z\s\.,]', ' ', line.upper()).strip()
                candidate = re.sub(r'\s+', ' ', candidate).strip()
                words = candidate.split()
                # Prefer names with 3+ words (first middle last)
                if len(words) >= 3 and len(candidate) > 15:
                    owner = candidate
                    break

    # Final cleanup
    owner = re.sub(r'\s+', ' ', owner).strip()

    return {
        'cr_plate_number': plate,
        'cr_brand': brand,
        'cr_color': color,
        'cr_year': year,
        'cr_owner_name': owner,
    }
