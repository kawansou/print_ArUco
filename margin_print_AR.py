import cv2, os
from cv2 import aruco
from fpdf import FPDF

# --- Parameters ---
dir_mark = './'  # Marker output directory
## ここに印刷したいマーカーIDを追加
marker_ids = [
              111, 112, 113, 114,  # Plum Rice Ball
              121, 122, 123, 124, 
              131, 132, 133, 134, 
              211, 212, 213, 214,  # Salmon Rice Ball
              221, 222, 223, 224, 
              231, 232, 233, 234, 
              311, 312, 313, 314,  # Tuna Rice Ball
              321, 322, 323, 324, 
              331, 332, 333, 334,
              411, 412, 413, 414,  # Sandwich
              421, 422, 423, 424,
              431, 432, 433, 434,
              511, 512, 513, 514, 515,  # Packed Juice
              521, 522, 523, 524, 525,
              531, 532, 533, 534, 535,
              611,  # Stick Salad
              621,
              631,
              711,  # Lunch Box1
              721,
              731,
              811,  # Lunch Box2
              821, 
              831,
              911,  # Coleslaw
              921,
              931,
              131, 231, 332, 434, 535  # 上段新品商品
              ]  # Marker IDs to generate
## 印刷したいマーカサイズを指定
######## --- marker_size_cm+rect_padding_cmが実際の印刷サイズになる
marker_size_cm = 1.6  # マーカのサイズ[cm]
rect_padding_cm = 0.4  # マーカの周りの余白サイズ[cm]
# --- Parameters ---




dpi = 300  # Print DPI for PDF (dots per inch)
marker_size_pixels = int(marker_size_cm / 2.54 * dpi)  # Convert cm to pixels
# spacing_pixels = int(spacing_mm / 10 * dpi)  # Convert mm to pixels
spacing_mm = 1.0  # Spacing between markers in mm
rect_padding_cm = rect_padding_cm / 2


# ArUco dictionary
dict_aruco = aruco.getPredefinedDictionary(aruco.DICT_4X4_1000)

# Create PDF
pdf = FPDF(orientation='L', unit='cm', format='A4')  # Landscape orientation
pdf.add_page()

# ページ設定 (例: A4サイズのランドスケープモード)
page_width_cm = 29.7  # A4の幅 (横)
page_height_cm = 21.0  # A4の高さ (縦)

# Initialize positions
x_position = 1  # Initial X position
y_position = 1  # Initial Y position

top_margin_cm = x_position  # Upper margin
bottom_margin_cm = y_position  # Lower margin

# Adjust marker size for the actual printable size
adjusted_marker_size_cm = marker_size_cm #* 2 / 0.9
adjusted_marker_size_pixels = int(adjusted_marker_size_cm / 2.54 * dpi)

try:
    for index, id_mark in enumerate(marker_ids):
        img_mark = aruco.generateImageMarker(dict_aruco, id_mark, marker_size_pixels)
        img_name_mark = f'mark_id_{id_mark}.jpg'
        path_mark = os.path.join(dir_mark, img_name_mark)

        # Save each marker as a temporary image
        cv2.imwrite(path_mark, img_mark)

        # Check line breaks for markers within page width
        if x_position + adjusted_marker_size_cm > page_width_cm - 1:
            x_position = 1  # Reset X position
            y_position += adjusted_marker_size_cm + spacing_mm + 0.5  # Increase Y position

        # Page break check for markers within page height
        if y_position + adjusted_marker_size_cm + bottom_margin_cm > page_height_cm:
            pdf.add_page()  # Add new page
            x_position = 1  # Reset X position
            y_position = top_margin_cm  # Reset Y position

        # Add marker image to PDF
        pdf.image(path_mark, x=x_position, y=y_position, w=adjusted_marker_size_cm)

        # Draw rectangle around the marker
        pdf.set_draw_color(245)  # Black color for rectangle
        pdf.rect(x_position - rect_padding_cm, y_position - rect_padding_cm, 
                 adjusted_marker_size_cm + 2 * rect_padding_cm, 
                 adjusted_marker_size_cm + 2 * rect_padding_cm)

        # Add ID number below the marker
        pdf.set_xy(x_position, y_position + adjusted_marker_size_cm + 0.5)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(adjusted_marker_size_cm, 0.4, f'ID: {id_mark}', align='C')

        # Update X position for the next marker
        x_position += adjusted_marker_size_cm + spacing_mm

    # Save the PDF
    pdf.output(os.path.join(dir_mark, "ArUco_margin.pdf"))
except Exception as e:
    print(f"Error: {e}")

# Clean up temporary image files
for id_mark in marker_ids:
    img_name_mark = f'mark_id_{id_mark}.jpg'
    path_mark = os.path.join(dir_mark, img_name_mark)
    if os.path.exists(path_mark):
        os.remove(path_mark)
