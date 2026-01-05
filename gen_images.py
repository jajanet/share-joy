import os
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

# --- CONFIG ---
WIDTH = 384  # Standard 58mm thermal printer width
FONT_PATH = "fonts/Noto_Sans_TC/static/NotoSansTC-Regular.ttf"
IMG_FOLDER = "images" 
OUTPUT_FOLDER = "to_print"
FONT_SIZE_MAIN = 22
FONT_SIZE_FOOTER = 16
PADDING = 20
PROJECT_LINK = "bit.ly/sf-joy-project" # Update this to your link

# --- DATASET ---
affirmations = [
    {"en": "Believe in yourself.", "es": "Cree en ti mismo.", "zh": "相信你自己。", "can": "要信自己。", "fil": "Magtiwala ka sa sarili."},
    {"en": "Take a deep breath.", "es": "Respira profundo.", "zh": "深呼吸一下。", "can": "唞啖大氣。", "fil": "Huminga nang malalim."},
    {"en": "Keep going.", "es": "Sigue adelante.", "zh": "繼續努力。", "can": "繼續加油！", "fil": "Laban lang."},
    {"en": "Be kind to yourself.", "es": "Sé amable contigo.", "zh": "對自己好一點。", "can": "對自己好啲。", "fil": "Maging mabait sa sarili."},
    {"en": "You're worthy of love and happiness.", "es": "Eres digno de amor y felicidad.", "zh": "你值得擁有愛與幸福。", "can": "你值得擁有愛同快樂。", "fil": "Karapat-dapat ka sa pag-ibig at kaligayahan."},
    {"en": "You and your flaws are loved, keep trying.", "es": "Tú y tus defectos son amados, sigue intentándolo.", "zh": "即便有缺點你也是被愛的，繼續努力。", "can": "就算有缺點都有人錫你，繼續試下啦。", "fil": "Mahal ka pati ang mga pagkukulang mo, sububukan lang."},
    {"en": "Your past doesn't define you, keep growing.", "es": "Tu pasado no te define, sigue creciendo.", "zh": "你的過去不能定義你，繼續成長。", "can": "你嘅過去定義唔到你，繼續成長。", "fil": "Hindi ka tinutukoy ng iyong nakaraan, patuloy na lumago."},
    {"en": "You are capable of so much.", "es": "Eres capaz de mucho.", "zh": "你的潛力無限。", "can": "你其實好叻，好有本事。", "fil": "Marami kang kayang gawin."},
    {"en": "I'm so glad you're here.", "es": "Me alegra mucho que estés aquí.", "zh": "我很高興你在這裡。", "can": "好開心可以見到你。", "fil": "Masaya ako na nandito ka."},
    {"en": "You deserve joy.", "es": "Mereces alegría.", "zh": "你值得擁有快樂。", "can": "你應得快樂嘅。", "fil": "Nararapat kang maging masaya."},
    {"en": "You have the power to create a life you desire.", "es": "Tienes el poder de crear la vida que deseas.", "zh": "你有力量去創造你想要的生活。", "can": "你有能力去創造你想過嘅生活。", "fil": "Nasa iyo ang kapangyarihan na likhain ang buhay na nais mo."},
    {"en": "You can overcome life's challenges.", "es": "Puedes superar los desafíos de la vida.", "zh": "你可以克服生活中的挑戰。", "can": "你可以克服生活上面嘅挑戰。", "fil": "Kaya mong lampasan ang mga hamon ng buhay."},
    {"en": "It's worth making life a little better everyday.", "es": "Vale la pena hacer la vida un poco mejor cada día.", "zh": "每天讓生活好一點點是值得的。", "can": "每日令生活好過啲係值得嘅。", "fil": "Sulit na gawing mas mabuti ang buhay araw-araw."},
    {"en": "Someone wants you to be happy.", "es": "Alguien quiere que seas feliz.", "zh": "有人希望你快樂。", "can": "有人好想你開心。", "fil": "May naghahangad na maging masaya ka."}
]

footer_data = {
    "en": "Keep this or pass it on to make someone smile.",
    "es": "Guárdalo para ti o compártelo para hacer sonreír a alguien.",
    "zh": "留給自己，或送給別人分享微笑。",
    "can": "留俾自己，或者送俾人分享下笑容。",
    "fil": "Itago para sa sarili, o ibahagi para makapagpangiti ng iba."
}

def text_wrap_draw(draw, text, font, y_start, font_size):
    """Wraps text for both Latin and CJK characters."""
    if any(ord(c) > 127 for c in text): # CJK / Accented check
        if any(ord(c) > 0x4E00 for c in text): # Chinese specific wrap
            max_chars = 14
            lines = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
        else: # Spanish/Filipino wrap
            lines = textwrap.wrap(text, width=28)
    else: # English wrap
        lines = textwrap.wrap(text, width=30)

    curr_y = y_start
    for line in lines:
        draw.text((WIDTH // 2, curr_y), line, font=font, fill=0, anchor="mt")
        curr_y += font_size + 6
    return curr_y + 8

def generate_strip(data, index):
    # Tall canvas, 1-bit mode (B&W)
    canvas = Image.new('1', (WIDTH, 4000), 1) 
    draw = ImageDraw.Draw(canvas)
    main_font = ImageFont.truetype(FONT_PATH, FONT_SIZE_MAIN)
    footer_font = ImageFont.truetype(FONT_PATH, FONT_SIZE_FOOTER)
    
    current_y = PADDING

    """
    # 1. GRAPHIC
    graphic_files = [f for f in os.listdir(IMG_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if graphic_files:
        with Image.open(os.path.join(IMG_FOLDER, random.choice(graphic_files))).convert("L") as icon:
            aspect = icon.height / icon.width
            new_w = WIDTH // 2
            new_h = int(new_w * aspect)
            icon = icon.resize((new_w, new_h), Image.Resampling.LANCZOS).convert("1")
            canvas.paste(icon, ((WIDTH - new_w) // 2, current_y))
            current_y += new_h + PADDING + 10
    """
    # 1. GRAPHIC (Raw paste, no resizing)
    graphic_files = [f for f in os.listdir(IMG_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if graphic_files:
        with Image.open(os.path.join(IMG_FOLDER, random.choice(graphic_files))) as icon:
            # Center the icon based on its actual width
            x_offset = (WIDTH - icon.width) // 2
            canvas.paste(icon, (x_offset, current_y))
            current_y += icon.height + PADDING

    # 2. AFFIRMATIONS
    for lang in ["en", "es", "zh", "can", "fil"]:
        current_y = text_wrap_draw(draw, data[lang], main_font, current_y, FONT_SIZE_MAIN)

    # 3. DIVIDER
    draw.line((WIDTH//4, current_y, 3*WIDTH//4, current_y), fill=0, width=1)
    current_y += PADDING

    # 4. FOOTER (Keep/Share + Link)
    for lang in ["en", "es", "zh", "can", "fil"]:
        current_y = text_wrap_draw(draw, footer_data[lang], footer_font, current_y, FONT_SIZE_FOOTER)
    
    draw.text((WIDTH // 2, current_y), f"Source: {PROJECT_LINK}", font=footer_font, fill=0, anchor="mt")
    current_y += FONT_SIZE_FOOTER + PADDING

    # 5. CROP & SAVE
    final_strip = canvas.crop((0, 0, WIDTH, current_y))
    final_strip.save(f"{OUTPUT_FOLDER}/strip_{index}.png")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_FOLDER): os.makedirs(OUTPUT_FOLDER)
    for i, aff in enumerate(affirmations):
        generate_strip(aff, i)
    print(f"Done. Check /{OUTPUT_FOLDER}")

