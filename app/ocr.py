import easyocr
import cv2
import os

# =====================================
# OCR READER
# =====================================

reader = easyocr.Reader(
    ['en'],
    gpu=False
)


# =====================================
# OCR FUNCTION
# =====================================

def extract_text(image_path):

    try:

        # =================================
        # CHECK IMAGE EXISTS
        # =================================

        if not os.path.exists(image_path):
            return ""

        # =================================
        # READ IMAGE
        # =================================

        image = cv2.imread(image_path)

        if image is None:
            return ""

        # =================================
        # RESIZE IMAGE
        # =================================

        image = cv2.resize(
            image,
            None,
            fx=3,
            fy=3,
            interpolation=cv2.INTER_CUBIC
        )

        # =================================
        # CONVERT TO GRAYSCALE
        # =================================

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        # =================================
        # DENOISE IMAGE
        # =================================

        gray = cv2.fastNlMeansDenoising(
            gray,
            None,
            10,
            7,
            21
        )

        # =================================
        # THRESHOLD
        # =================================

        thresh = cv2.adaptiveThreshold(

            gray,

            255,

            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

            cv2.THRESH_BINARY,

            11,

            2
        )

        # =================================
        # SAVE TEMP IMAGE
        # =================================

        os.makedirs("uploads", exist_ok=True)

        temp_path = "uploads/temp_ocr.png"

        cv2.imwrite(temp_path, thresh)

        # =================================
        # OCR EXTRACTION
        # =================================

        results = reader.readtext(

            temp_path,

            detail=0,

            paragraph=False
        )

        # =================================
        # CLEAN OCR TEXT
        # =================================

        cleaned_lines = []

        for line in results:

            line = line.strip()

            if len(line) < 2:
                continue

            # remove garbage symbols
            line = line.replace("@", "")
            line = line.replace("|", "")
            line = line.replace("€", "C")
            line = line.replace("¢", "c")
            line = line.replace("™", "")
            line = line.replace("~", "")
            line = line.replace("_", " ")

            cleaned_lines.append(line)

        extracted_text = "\n".join(cleaned_lines)

        # =================================
        # DEBUG PRINT
        # =================================

        print("\n========== OCR TEXT ==========\n")
        print(extracted_text)
        print("\n==============================\n")

        return extracted_text

    except Exception as e:

        print("OCR ERROR:", str(e))

        return ""