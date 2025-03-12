from rubpy import Client, filters
from rubpy.types import Updates
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os
import random

def add_timestamp_to_image(input_image_path, output_image_path, font_path="arial.ttf", font_size=60, text_color=(255, 255, 255), background_color=(0, 0, 0, 128)):
  
    try:
        
        image = Image.open(input_image_path).convert("RGBA")
        

        overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        font = ImageFont.truetype(font_path, font_size)
        
  
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
 
        text_width, text_height = draw.textsize(current_time, font=font)
        

        x = (image.width - text_width) // 2
        y = (image.height - text_height) // 2
        

        draw.rectangle((x - 10, y - 10, x + text_width + 10, y + text_height + 10), fill=background_color)
        

        draw.text((x, y), current_time, font=font, fill=text_color)
        

        final_image = Image.alpha_composite(image, overlay)
        
     
        final_image.save(output_image_path, "PNG")
        print(f"زمان دقیق ({current_time}) با موفقیت به عکس اضافه شد و در {output_image_path} ذخیره شد.")
    except Exception as e:
        print(f"خطا در پردازش عکس: {e}")

bot = Client(name='timestamp_to_image')
guid_bot=""
@bot.on_message_updates(filters.is_private)
async def updates(update: Updates):
    if update.text == "تایم":
        try:
         
            input_folder = "images"
            output_folder = "processed_images"
            
        
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            
         
            processed_images = []
            
    
            for filename in os.listdir(input_folder):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    input_image_path = os.path.join(input_folder, filename)
                    output_image_path = os.path.join(output_folder, f"processed_{filename}")
                    
            
                    add_timestamp_to_image(input_image_path, output_image_path)
                    
                 
                    processed_images.append(output_image_path)
     
            if processed_images:
           
                selected_image = random.choice(processed_images)
                
          
                await bot.upload_avatar(guid_bot, selected_image)
                
              
                await update.reply("تمام عکس‌ها با موفقیت پردازش شدند و یک عکس به‌عنوان پروفایل آپلود شد.")
            else:
                await update.reply("هیچ عکسی برای پردازش یافت نشد.")
        except Exception as e:
            await update.reply(f"خطا در پردازش عکس‌ها: {e}")

bot.run()
