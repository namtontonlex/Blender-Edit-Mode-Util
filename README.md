# Blender-Edit-Mode-Util
Utility Tools for blender Edit Mode
เครื่องมือรวมคำสั่งอำนวยความสะดวกสำหรับ Edit Mode ใน Blender โดยเน้นไปที่การดูดติดพื้นผิว (Surface Snapping) และการล็อกตำแหน่งจุด (Vertex Locking)
🛠 ฟีเจอร์หลัก

    Surface Snap Brush: แปรงสำหรับดูด Vertex ให้แนบไปกับพื้นผิวของวัตถุอื่นในฉากทันที

    Vertex Lock Tool: ล็อกตำแหน่ง Vertex ไม่ให้เคลื่อนที่แม้จะเผลอไปกด Move โดยจะแสดงไฮไลต์สีม่วงให้เห็นชัดเจน

📥 วิธีการติดตั้ง

    ดาวน์โหลดไฟล์ Edit_Mode_Util.py จาก GitHub นี้

    เปิดโปรแกรม Blender ไปที่ Edit > Preferences > Add-ons

    คลิกปุ่ม Install... แล้วเลือกไฟล์ที่ดาวน์โหลดมา

    ติ๊กถูกหน้าชื่อ Mesh: Edit_Mode_Util เพื่อเปิดใช้งาน

🚀 วิธีใช้งาน

แถบเครื่องมือจะอยู่ที่ 3D Viewport > Side Panel (กด N) > แถบ Edit Util
1. Surface Snap

    กดปุ่ม Start Snap Brush (ต้องอยู่ใน Edit Mode)

    คลิกซ้ายค้าง: เพื่อถูแปรงลงบนจุดที่ต้องการให้ดูดติดผิววัตถุอื่น

    ปุ่ม [ และ ]: ใช้ปรับขนาดวงล้อแปรง

    ESC หรือ คลิกขวา: เพื่อออกจากโหมดแปรง

2. Vertex Lock

    เลือก Vertex ที่ต้องการล็อก

    กดปุ่ม Lock (Alt + Space): จุดที่เลือกจะกลายเป็นสีม่วงและไม่สามารถขยับได้

    กดปุ่ม Unlock All (Ctrl + Alt + Space): เพื่อปลดล็อกจุดทั้งหมดในวัตถุนั้น

⚖️ License

เผยแพร่ภายใต้สัญญาอนุญาต GNU GPL v3 (สอดคล้องกับมาตรฐาน Blender Add-on)
