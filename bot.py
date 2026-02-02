from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import BadRequest

# API KEY (Bot Token)
BOT_TOKEN = '8224462231:AAFBAW-jigafWbEWuQLtoMbOYhl3Q15Zqs0'

# Global Materials Library
# Structure: stream_subject -> { category -> content }
MATERIALS = {
    'jee_physics': {
        'notes': (
            "📝 *JEE/NEET Physics - Notes & Resources*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"

        ),
        'books': (
            "📚 *JEE/NEET Physics - Standard Books*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "• ARJUNA JEE (2025) PHYSICS MODULE 2: [Download](https://jee-materials-bot.blogspot.com/2026/01/arjuna-jee-2025-physics-module-2_01413026203.html)\n"
            "• ARJUNA JEE (2025) PHYSICS MODULE 3: [Download](https://jee-materials-bot.blogspot.com/2026/01/arjuna-jee-2025-physics-module-3_01361103017.html)\n"
            "• ARJUNA JEE (2025) PHYSICS MODULES 4: [Download](https://jee-materials-bot.blogspot.com/2026/01/arjuna-jee-2025-physics-modules-4_0529309805.html)\n"
            "• B. M. Sharma - Electrostatics and Current Electricity for JEE (Advanced)-CENGAGE INDIA (2019) (1): [Download](https://jee-materials-bot.blogspot.com/2026/01/b-m-sharma-electrostatics-and-current_01959555478.html)\n"
            "• B. M. Sharma - Optics and Modern Physics for JEE (Advanced)-CENGAGE INDIA (2019)_11zon: [Download](https://jee-materials-bot.blogspot.com/2026/01/b-m-sharma-optics-and-modern-physics_01726081198.html)\n"
            "• B. M. Sharma - Waves & Thermodynamics for JEE (Advanced)-CENGAGE INDIA (2019): [Download](https://jee-materials-bot.blogspot.com/2026/01/b-m-sharma-waves-thermodynamics-for-jee_018844099.html)\n"
            "• B.M Sharma - Physics For IIT-JEE 2012-2013 _ Mechanics - I-Cengage (2012): [Download](https://jee-materials-bot.blogspot.com/2026/01/bm-sharma-physics-for-iit-jee-2012-2013_0326850158.html)\n"
            "• B.M Sharma - Physics For IIT-JEE 2012-2013 _ Mechanics - II-Cengage (2012): [Download](https://jee-materials-bot.blogspot.com/2026/01/bm-sharma-physics-for-iit-jee-2012-2013_01274091687.html)\n"
            "• DC PANDEY ELECTRICITY AND MAGNETISM ( COMPLETE ): [Download](https://jee-materials-bot.blogspot.com/2026/01/dc-pandey-electricity-and-magnetism_0583098761.html)\n"
            "• DC PANDEY MECHANICS 1: [Download](https://jee-materials-bot.blogspot.com/2026/01/dc-pandey-mechanics-1.html)\n"
            "• DC PANDEY MECHANICS 2: [Download](https://jee-materials-bot.blogspot.com/2026/01/dc-pandey-mechanics-2_0183089731.html)\n"
            "• DC PANDEY OPTICS AND MODERN PHYSICS ( COMPLETE ): [Download](https://jee-materials-bot.blogspot.com/2026/01/dc-pandey-optics-and-modern-physics_0310171688.html)\n"
            "• dc-pandey-physics-pdf-945d46f5: [Download](https://jee-materials-bot.blogspot.com/2026/01/dc-pandey-physics-pdf-945d46f5.html)\n"
            "• JEE_Physics_Complete_Module: [Download](https://jee-materials-bot.blogspot.com/2026/01/jeephysicscompletemodule.html)\n"
            "• Kinematics__HC_Verma__5_with_anno: [Download](https://jee-materials-bot.blogspot.com/2026/01/kinematicshcverma5withanno.html)\n"
            "• LAKSHYA JEE  PHYSICS MODULE 01: [Download](https://jee-materials-bot.blogspot.com/2026/01/lakshya-jee-physics-module-01.html)\n"
            "• LAKSHYA JEE  PHYSICS MODULE 2: [Download](https://jee-materials-bot.blogspot.com/2026/01/lakshya-jee-physics-module-2.html)\n"
            "• LAKSHYA JEE PHYSICS MODULE 3: [Download](https://jee-materials-bot.blogspot.com/2026/01/lakshya-jee-physics-module-3.html)\n"
            "• LAKSHYA JEE PHYSICS MODULE 4: [Download](https://jee-materials-bot.blogspot.com/2026/01/lakshya-jee-physics-module-4.html)\n"
            "• LakshyaJeePhysicsSolutionModule: [Download](https://jee-materials-bot.blogspot.com/2026/01/lakshyajeephysicssolutionmodule.html)\n"
            "• SKC Physics Crush Class 11 By @StudyShelf: [Download](https://jee-materials-bot.blogspot.com/2026/01/skc-physics-crush-class-11-by-studyshelf.html)\n"
            "• Waves & Thermodynamics-DC Pandey: [Download](https://jee-materials-bot.blogspot.com/2026/01/waves-thermodynamics-dc-pandey.html)\n"
        ),
        'pyqs': (
            "❓ *All JEE Papers*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"

        )
    },
    'jee_chemistry': {
        'notes': (
            "📝 *JEE Chemistry - Notes & Resources*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "• Kattar_Advanced_EaJEE_Notes_for_Inorganic_Chemistry_Class_11th+12th: [Download](https://jee-materials-bot.blogspot.com/2026/02/kattaradvancedeajeenotesforinorganicche.html)\n"
        ),
        'books': (
            "📚 *JEE Chemistry - Standard Books & Resources*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "• ARJUNA JEE (2025) CHEMISTRY MODULES 2: [Download](https://jee-materials-bot.blogspot.com/2026/02/arjuna-jee-2025-chemistry-modules-2.html)\n"
            "• ARJUNA JEE (2025) CHEMISTRY MODULES 3: [Download](https://jee-materials-bot.blogspot.com/2026/02/arjuna-jee-2025-chemistry-modules-3.html)\n"
            "• ARJUNA JEE (2025) CHEMISTRY MODULES 4: [Download](https://jee-materials-bot.blogspot.com/2026/02/arjuna-jee-2025-chemistry-modules-4.html)\n"
            "• ARJUNA JEE (2025) CHEMISTRY MODULES 4_1769703995: [Download](https://jee-materials-bot.blogspot.com/2026/02/arjuna-jee-2025-chemistry-modules.html)\n"
            "• JEE_Chemistry_Complete_Module: [Download](https://jee-materials-bot.blogspot.com/2026/02/jeechemistrycompletemodule.html)\n"
            "• Lakshya Jee Chemistry Module 3: [Download](https://jee-materials-bot.blogspot.com/2026/02/lakshya-jee-chemistry-module-3.html)\n"
            "• LakshyaJeeChemistryModule1: [Download](https://jee-materials-bot.blogspot.com/2026/02/lakshyajeechemistrymodule1.html)\n"
            "• LakshyaJeeChemistryModule2: [Download](https://jee-materials-bot.blogspot.com/2026/02/lakshyajeechemistrymodule2.html)\n"
            "• LakshyaJeeChemistryModule4: [Download](https://jee-materials-bot.blogspot.com/2026/02/lakshyajeechemistrymodule4.html)\n"
            "• LakshyaJeeChemistrySolutionModule: [Download](https://jee-materials-bot.blogspot.com/2026/02/lakshyajeechemistrysolutionmodule.html)\n"
        ),


        'pyqs': (
            "❓ *All JEE Papers*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"

        )
    },
    'jee_maths': {
        'notes': (
            "📝 *JEE Maths - Notes & Resources*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"


        ),
        'books': (
            "📚 *JEE Maths Books*\n\n[Cengage](...)\n[Arihant](...)\n"
            "• LakshyaJeeMathsModule11: [Download](https://jee-materials-bot.blogspot.com/2026/02/lakshyajeemathsmodule11.html)\n"
            "• LakshyaJeeMathsModule2: [Download](https://jee-materials-bot.blogspot.com/2026/02/lakshyajeemathsmodule2.html)\n"
            "• LakshyaJeeMathsModule3: [Download](https://jee-materials-bot.blogspot.com/2026/02/lakshyajeemathsmodule3.html)\n"
            "• LakshyaJeeMathsModule4: [Download](https://jee-materials-bot.blogspot.com/2026/02/lakshyajeemathsmodule4.html)\n"
            "• maths-Aptitude-Book: [Download](https://jee-materials-bot.blogspot.com/2026/02/maths-aptitude-book.html)\n"
        ),
        'pyqs': (
            "❓ *All JEE Papers*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
        )

    },
    'neet_physics': {
        'notes': (
            "📝 *JEE/NEET Physics - Notes & Resources*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"


        ),
        'books': (
            "📚 *JEE/NEET Physics - Standard Books*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "• ARJUNA JEE (2025) PHYSICS MODULE 2: [Download](https://jee-materials-bot.blogspot.com/2026/01/arjuna-jee-2025-physics-module-2_01413026203.html)\n"
            "• ARJUNA JEE (2025) PHYSICS MODULE 3: [Download](https://jee-materials-bot.blogspot.com/2026/01/arjuna-jee-2025-physics-module-3_01361103017.html)\n"
            "• ARJUNA JEE (2025) PHYSICS MODULES 4: [Download](https://jee-materials-bot.blogspot.com/2026/01/arjuna-jee-2025-physics-modules-4_0529309805.html)\n"
            "• B. M. Sharma - Electrostatics and Current Electricity for JEE (Advanced)-CENGAGE INDIA (2019) (1): [Download](https://jee-materials-bot.blogspot.com/2026/01/b-m-sharma-electrostatics-and-current_01959555478.html)\n"
            "• B. M. Sharma - Optics and Modern Physics for JEE (Advanced)-CENGAGE INDIA (2019)_11zon: [Download](https://jee-materials-bot.blogspot.com/2026/01/b-m-sharma-optics-and-modern-physics_01726081198.html)\n"
            "• B. M. Sharma - Waves & Thermodynamics for JEE (Advanced)-CENGAGE INDIA (2019): [Download](https://jee-materials-bot.blogspot.com/2026/01/b-m-sharma-waves-thermodynamics-for-jee_018844099.html)\n"
            "• B.M Sharma - Physics For IIT-JEE 2012-2013 _ Mechanics - I-Cengage (2012): [Download](https://jee-materials-bot.blogspot.com/2026/01/bm-sharma-physics-for-iit-jee-2012-2013_0326850158.html)\n"
            "• B.M Sharma - Physics For IIT-JEE 2012-2013 _ Mechanics - II-Cengage (2012): [Download](https://jee-materials-bot.blogspot.com/2026/01/bm-sharma-physics-for-iit-jee-2012-2013_01274091687.html)\n"
            "• DC PANDEY ELECTRICITY AND MAGNETISM ( COMPLETE ): [Download](https://jee-materials-bot.blogspot.com/2026/01/dc-pandey-electricity-and-magnetism_0583098761.html)\n"
            "• DC PANDEY MECHANICS 1: [Download](https://jee-materials-bot.blogspot.com/2026/01/dc-pandey-mechanics-1.html)\n"
            "• DC PANDEY MECHANICS 2: [Download](https://jee-materials-bot.blogspot.com/2026/01/dc-pandey-mechanics-2_0183089731.html)\n"
            "• DC PANDEY OPTICS AND MODERN PHYSICS ( COMPLETE ): [Download](https://jee-materials-bot.blogspot.com/2026/01/dc-pandey-optics-and-modern-physics_0310171688.html)\n"
            "• dc-pandey-physics-pdf-945d46f5: [Download](https://jee-materials-bot.blogspot.com/2026/01/dc-pandey-physics-pdf-945d46f5.html)\n"
            "• JEE_Physics_Complete_Module: [Download](https://jee-materials-bot.blogspot.com/2026/01/jeephysicscompletemodule.html)\n"
            "• Kinematics__HC_Verma__5_with_anno: [Download](https://jee-materials-bot.blogspot.com/2026/01/kinematicshcverma5withanno.html)\n"
            "• LAKSHYA JEE  PHYSICS MODULE 01: [Download](https://jee-materials-bot.blogspot.com/2026/01/lakshya-jee-physics-module-01.html)\n"
            "• LAKSHYA JEE  PHYSICS MODULE 2: [Download](https://jee-materials-bot.blogspot.com/2026/01/lakshya-jee-physics-module-2.html)\n"
            "• LAKSHYA JEE PHYSICS MODULE 3: [Download](https://jee-materials-bot.blogspot.com/2026/01/lakshya-jee-physics-module-3.html)\n"
            "• LAKSHYA JEE PHYSICS MODULE 4: [Download](https://jee-materials-bot.blogspot.com/2026/01/lakshya-jee-physics-module-4.html)\n"
            "• LakshyaJeePhysicsSolutionModule: [Download](https://jee-materials-bot.blogspot.com/2026/01/lakshyajeephysicssolutionmodule.html)\n"
            "• SKC Physics Crush Class 11 By @StudyShelf: [Download](https://jee-materials-bot.blogspot.com/2026/01/skc-physics-crush-class-11-by-studyshelf.html)\n"
            "• Waves & Thermodynamics-DC Pandey: [Download](https://jee-materials-bot.blogspot.com/2026/01/waves-thermodynamics-dc-pandey.html)\n"
        ),
        'pyqs': (
            "❓ *NEET Physics PYQs*\n\n[2023](...)\n[2022](...)\n"
        ),
    },
    'neet_chemistry': {
        'notes': (
            "📝 *JEE/NEET Chemistry - Notes & Resources*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"

        ),
        'books': (
            "📚 *JEE/NEET Chemistry - Standard Books & Resources*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"

        ),
        'pyqs': (
            "❓ *NEET Chemistry PYQs*\n\n[2023](...)\n[2022](...)\n"
        ),
    },
    'neet_biology': {
        'notes': (
            "📝 *NEET Biology Notes*\n\n[Link 1](...)\n[Link 2](...)\n"
            "• POCKET BOOK (11th) By Anand mani.pdf: [Download](https://jee-materials-bot.blogspot.com/2026/01/pocket-book-11th-by-anand-mani.html)\n"
            "• POCKET BOOK (12th) By Anand Mani.pdf: [Download](https://jee-materials-bot.blogspot.com/2026/01/pocket-book-12th-by-anand-mani.html)\n"
        ),
        'books': (
            "📚 *NEET Biology - Standard Books & Resources*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            

        ),
        'pyqs': (
            "❓ *NEET Biology PYQs*\n\n[2023](...)\n[2022](...)\n"
        ),
    }
}

# --- Helper Functions for Menus ---

def get_main_menu():
    keyboard = [
        [
            InlineKeyboardButton("👨‍🎓 JEE / IIT", callback_data="menu_jee"),
            InlineKeyboardButton("👨‍⚕️ NEET / Medical", callback_data="menu_neet")
        ],
        [InlineKeyboardButton("ℹ️ About Us", callback_data="about")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_jee_menu():
    keyboard = [
        [InlineKeyboardButton("⚡️ Physics", callback_data="sub_jee_physics"), 
         InlineKeyboardButton("🧪 Chemistry", callback_data="sub_jee_chemistry")],
        [InlineKeyboardButton("📐 Maths", callback_data="sub_jee_maths")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_neet_menu():
    keyboard = [
        [InlineKeyboardButton("🔭 Physics", callback_data="sub_neet_physics"), 
         InlineKeyboardButton("🧪 Chemistry", callback_data="sub_neet_chemistry")],
        [InlineKeyboardButton("🧬 Biology", callback_data="sub_neet_biology")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_type_menu(subject_key):
    # Determine label for PYQs based on exam type
    exam_type = "JEE" if "jee" in subject_key else "NEET"
    
    keyboard = [
        [InlineKeyboardButton("📝 Notes", callback_data=f"show_{subject_key}_notes"),
         InlineKeyboardButton("📚 Books", callback_data=f"show_{subject_key}_books")],
        [InlineKeyboardButton(f"❓ All {exam_type} Papers", callback_data=f"show_{subject_key}_pyqs")],
        [InlineKeyboardButton("🔙 Back", callback_data=f"menu_{subject_key.split('_')[0]}")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_button(back_to_callback):
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data=back_to_callback)]]
    return InlineKeyboardMarkup(keyboard)

# --- Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # You can also use await update.message.reply_photo("IMAGE_URL", caption="...") if you have a logo
    await update.message.reply_text(
        (
            "🎓 *Welcome to Jee & Neet Materials Bot* 🎓\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "We provide premium study materials, notes, and PYQs.\n\n"
            "👇 *Select your stream below:*"
        ),
        parse_mode='Markdown',
        reply_markup=get_main_menu()
    )

async def description_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Free Study Material Bot: Physics, Chem, Maths & Bio Notes + Books + PYQs for JEE & NEET."
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()
    except BadRequest:
        pass # Ignore if query is too old
    data = query.data
    
    # 1. Main Navigation
    if data == "main_menu":
        await query.edit_message_text(
            text="🎓 *Main Menu* 🎓\n━━━━━━━━━━━━━━━━━━━━\nSelect your target exam:",
            parse_mode='Markdown', reply_markup=get_main_menu()
        )
    
    elif data == "menu_jee":
        await query.edit_message_text(
            text="👨‍🎓 *JEE Aspirants Zone*\n━━━━━━━━━━━━━━━━━━━━\nSelect your subject:", 
            parse_mode='Markdown', reply_markup=get_jee_menu()
        )
        
    elif data == "menu_neet":
        await query.edit_message_text(
            text="👨‍⚕️ *NEET Aspirants Zone*\n━━━━━━━━━━━━━━━━━━━━\nSelect your subject:", 
            parse_mode='Markdown', reply_markup=get_neet_menu()
        )

    # 2. Subject Selection (Intermediate Step) -> Show separated types
    elif data.startswith("sub_"):
        subject_key = data[4:] # e.g., jee_physics
        display_name = subject_key.replace('_', ' ').title()
        
        await query.edit_message_text(
            text=f"📂 *{display_name} Material*\n━━━━━━━━━━━━━━━━━━━━\nWhat are you looking for?", 
            parse_mode='Markdown', 
            reply_markup=get_type_menu(subject_key)
        )

    # 3. Final Content Display
    elif data.startswith("show_"):
        # Format: show_jee_physics_notes
        parts = data.split('_') # ['show', 'jee', 'physics', 'notes']
        category_type = parts[-1] # 'notes'
        subject_key = f"{parts[1]}_{parts[2]}" # 'jee_physics'
        
        # Safe fetch
        subject_data = MATERIALS.get(subject_key, {})
        content = subject_data.get(category_type, "⚠️ Content coming soon!")
        
        # Back button goes back to the Type Selection menu for this subject
        back_callback = f"sub_{subject_key}"
        
        await query.edit_message_text(
            text=content, 
            parse_mode='Markdown', 
            disable_web_page_preview=True, 
            reply_markup=get_back_button(back_callback)
        )

    elif data == "about":
        await query.answer("Created with ❤️ for Students.", show_alert=True)

if __name__ == '__main__':
    print("Bot is starting...")
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler("description", description_command))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("Polling...")
    application.run_polling()
# Added: B.M Sharma - Physics For IIT-JEE 2012-2013 _ Mechanics - I-Cengage (2012).pdf -> https://jee-materials-bot.blogspot.com/2026/01/bm-sharma-physics-for-iit-jee-2012-2013.html [jee_physics/books]