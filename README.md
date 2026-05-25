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


<img width="714" height="475" alt="Snap" src="https://github.com/user-attachments/assets/ff0b7848-6bc5-470b-bfe7-bb06df2ef050" />

1. Surface Snap

    กดปุ่ม Start Snap Brush (ต้องอยู่ใน Edit Mode)

    คลิกซ้ายค้าง: เพื่อถูแปรงลงบนจุดที่ต้องการให้ดูดติดผิววัตถุอื่น

    ปุ่ม [ และ ]: ใช้ปรับขนาดวงล้อแปรง

    ESC หรือ คลิกขวา: เพื่อออกจากโหมดแปรง
   


<img width="783" height="596" alt="Lock" src="https://github.com/user-attachments/assets/2f4bfc5a-bda5-44c7-b7fe-a4359aa178b5" />

2. Vertex Lock

    เลือก Vertex ที่ต้องการล็อก

    กดปุ่ม Lock (Alt + Space): จุดที่เลือกจะกลายเป็นสีม่วงและไม่สามารถขยับได้

    กดปุ่ม Unlock All (Ctrl + Alt + Space): เพื่อปลดล็อกจุดทั้งหมดในวัตถุนั้น

⚖️ License

เผยแพร่ภายใต้สัญญาอนุญาต GNU GPL v3 (สอดคล้องกับมาตรฐาน Blender Add-on)

* สาระสำคัญ
  
    1.นำไปใช้ได้ฟรีทั้งส่วนตัวและเชิงพานิชย์
  
    2.แก้ไขและเผยแพร่ได้แต่ต้องเผยแพร่โค้ดทั้งหมดด้วย


Edit_Mode_Util

Integrated tools for Surface Snapping and Vertex Locking in Blender Edit Mode.
Features

    Interactive Surface Snap: Allows you to interactively snap vertices to a target mesh surface using a brush-like tool.

    Vertex Lock: Lock specific vertices in place to prevent accidental movement, with visual feedback.

Installation

    Download this repository as a .zip file.

    Open Blender.

    Go to Edit > Preferences > Add-ons > Install...

    Select the downloaded zip file.

    Enable the "Edit_Mode_Util" add-on.

Usage

    Surface Snap: Open the "Edit Util" panel in the N-panel (Side bar) while in Edit Mode.

    Vertex Lock: Select vertices, then use the "Lock" button or press Alt + Space. Use Ctrl + Alt + Space to unlock all.

License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

By using, modifying, or distributing this software, you agree to the terms of the GPL-3.0 license. You can find a copy of the license in the LICENSE file included in this repository, or at https://www.gnu.org/licenses/gpl-3.0.html.
