import pygame as pg
from datetime import datetime
import time
from sys import exit
from json import load, dump

order = None
newmenu = None

def makeReceipt(order):
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M")
    tax = order.get_price()*0.27
    subtotal = order.get_price()-tax
    total = order.get_price()
    items = order.items
    change = order.paid - order.get_price()
    method = order.paymentmethod
    sample = [
        "=======================================",
        "  VAJKYPOS V2 ÉRTÉKESÍTÉSI BIZONYLAT   ",
        "=======================================",
        "",
        "Dátum: [date]",
        "Idő: [time]",
        "Rendelés: [num]",
        "",
        "---------------------------------------",
        "Termék           Mennyiség    Egységár",
        "---------------------------------------",
        "[items]",
        "---------------------------------------",
        "",
        "Részösszeg:      [subtotal]",
        "Adó:             [tax]",
        "Összesen:        [total]",
        "",
        "Fizetési mód:    [paymentmethod]",
        "Fizetve:         [paid]",
        "Visszajáró:      [change]",
        "",
        "Köszönjük a vásárlást!",
        "",
        "=======================================",
        "              AP:  [AP]                "
    ]

    receipt = []
    for row in sample:
        try:
            row = row.replace("[date]", date)
        except:
            pass
        try:
            row = row.replace("[time]", time)
        except:
            pass
        try:
            row = row.replace("[num]", str(order.num))
        except:
            pass
        if "[items]" in row:
            row = ""
            for item in items:
                name = item["name"]
                price = str(item["price"]) + "Ft"
                qty = str(item["count"])

                space1 = 18
                space2 = 13

                row += name
                for _ in range(space1 - len(name)):
                    row += " "
                row += qty
                for _ in range(space2 - len(qty)):
                    row += " "
                row += price + "\n"
                if item["type"] == "menu":
                    for subitem in item["items"]:
                        row += " -> " + subitem["name"] + "\n"
        try:
            row = row.replace("[subtotal]", str(subtotal) + "Ft")
        except:
            pass
        try:
            row = row.replace("[tax]", str(tax) + "Ft")
        except:
            pass
        try:
            row = row.replace("[total]", str(total) + "Ft")
        except:
            pass
        try:
            row = row.replace("[change]", str(change) + "Ft")
        except:
            pass
        try:
            row = row.replace("[paymentmethod]", method)
        except:
            pass
        try:
            row = row.replace("[paid]", str(order.paid) + "Ft")
        except:
            pass

        receipt.append(row + "\n")
        with open("save_receipt.txt", "w", encoding="utf-8") as saveReceipt:
            for row in receipt:
                saveReceipt.write(row)
            print("receipt written to save_receipt.txt")


def error(error, code="000", file="n/a", exception="n/a"):
    giantfont = pg.font.Font("assets/fonts/sysfont_extrabold.ttf", int(0.09 * w))
    font_bold = pg.font.Font("assets/fonts/sysfont_bold.ttf", int(0.02 * w))
    font = pg.font.Font("assets/fonts/sysfont.ttf", int(0.02 * w))
    logo = pg.transform.scale(pg.image.load("assets/img/logo.png"), (int(639 / 3000 * w), int(368 / 3000 * w)))
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_RETURN:
                    exit()

        screen.fill((255, 50, 50))
        screen.blit(logo, logo.get_rect(center=(w/2, 10 + logo.get_height()/2.5)))
        error_title = giantfont.render("HIBA", True, fontcolor)
        error_subtitle = font_bold.render("Kritikus hiba történt a progam futása közben", True, fontcolor)

        pg.draw.rect(surface, (150, 0, 0), (w/8, h/2-100, w-w/4, h/2+50), border_radius=30)
        pg.draw.rect(surface, (255, 255, 255), (w/8, h/2-100, w-w/4, h/2+50), 5, border_radius=30)

        if error == "load-interface":
            errortext = "A program nem tudja beolvasni az interfész információit tartalmazó fájlt. Kérjük, indítsd újra a rendszert és próbáld újra. A nem mentett adatok elvesznek. Ha a probléma továbbra is fennáll, kérjük vedd fel a kapcsolatot a rendszergazdával. Az alábbi hibakód segíthet a hiba azonosításában."
        elif error == "load-images":
            errortext = "A program nem tudja betölteni valamely ikonokat vagy képeket. Kérjük, indítsd újra a rendszert és próbáld újra. A nem mentett adatok elvesznek. Ha a probléma továbbra is fennáll, kérjük vedd fel a kapcsolatot a rendszergazdával. Az alábbi hibakód segíthet a hiba azonosításában."
        elif error == "general":
            errortext = "A program kódhibába ütközött. A hiba feltehetőleg azért keletkezett, mert egy hulladék a kód. Kérjük, indítsd újra a rendszert és próbáld újra. A nem mentett adatok elvesznek. Ha a probléma továbbra is fennáll, kérjük vedd fel a kapcsolatot a rendszergazdával. Az alábbi hibakód segíthet a hiba azonosításában."
        elif error == "load-fonts":
            errortext = "A program nem tudja betölteni a program futásához szükséges betűstílusokat. Kérjük, indítsd újra a rendszert és próbáld újra. A nem mentett adatok elvesznek. Ha a probléma továbbra is fennáll, kérjük vedd fel a kapcsolatot a rendszergazdával. Az alábbi hibakód segíthet a hiba azonosításában."
        elif error == "load-presets":
            errortext = "A program nem tudja betölteni a kijelzőméret konfigurációját. Kérjük indítsd újra a rendszert és próbáld újra. A nem mentett adatok elvesznek. Ha a probléma továbbra is fennáll, kérjük vedd fel a kapcsolatot a rendszergazdával. Az alábbi hibakód segíthet a hiba azonosításában."
        else:
            errortext = "Ismeretlen hiba lépett fel a program futása közben. A program nem tud elindulni. Kérjuk, indítsd újra a rendszert és próbáld újra. A nem mentett adatok elvesznek. Ha a probléma továbbra is fennáll, kérjük vedd fel a kapcsolatot a rendszergazdával. Az alábbi hibakód segíthet a hiba azonosításában."

        error_detail1 = font.render(f"Érintett fájl: {file}, Hiba kódja: {code}", True, fontcolor)
        error_detail2 = font.render(f"{type(exception).__name__} - {exception}", True, fontcolor)

        screen.blit(error_title, error_title.get_rect(center=(w/2, h/3.6)))
        screen.blit(error_subtitle, error_subtitle.get_rect(center=(w/2, h/2-50)))
        wordsrow1 = ""
        wordsrow2 = ""
        wordsrow3 = ""
        wordsrow4 = ""
        wordsrow5 = ""
        for word in errortext.split(" "):
            if font.size(wordsrow1)[0] < w-w/3-150:
                wordsrow1 += word + " "
            elif font.size(wordsrow2)[0] < w-w/3-150:
                wordsrow2 += word + " "
            elif font.size(wordsrow3)[0] < w-w/3-150:
                wordsrow3 += word + " "
            elif font.size(wordsrow4)[0] < w-w/3-150:
                wordsrow4 += word + " "
            elif font.size(wordsrow5)[0] < w-w/3-150:
                wordsrow5 += word + " "
        row1 = wordsrow1
        row2 = wordsrow2
        try:
            row3 = wordsrow3
        except:
            row3 = ""
        try:
            row4 = wordsrow4
        except:
            row4 = ""
        try:
            row5 = wordsrow5
        except:
            row5 = ""
        screen.blit(font.render(row1, True, fontcolor), (w/8+50, h/2))
        screen.blit(font.render(row2, True, fontcolor), (w/8+50, h/2+50))
        screen.blit(font.render(row3, True, fontcolor), (w/8+50, h/2+100))
        screen.blit(font.render(row4, True, fontcolor), (w/8+50, h/2+150))
        screen.blit(font.render(row5, True, fontcolor), (w/8+50, h/2+200))
        screen.blit(font.render("Hibanapló:", True, fontcolor), (w/8+50, h/2+250))
        screen.blit(error_detail1, error_detail1.get_rect(topleft=(w/8+50, h/2+300)))
        screen.blit(error_detail2, error_detail2.get_rect(topleft=(w/8+50, h/2+350)))

        pg.display.flip()

def draw_if():
    global switch_view, button_sizing
    bw_double, bw_triple, bw_quadruple = button_sizing
    rowcount = 0
    colcount = 0
    buttons = interface[switch_view]

    for row in buttons:
        for button in row:
            #button box
            try:
                if button["buttonsize"] == "double":
                    bw = bw_double
                    tw = 2.4
                elif button["buttonsize"] == "triple":
                    bw = bw_triple
                    tw = 3.4
                elif button["buttonsize"] == "quadruple":
                    bw = bw_quadruple
                    tw = 5.5
            except:
                bw = 1
                tw = 1
                pass
            if button["buttontype"] == "blank":
                pass
            else:
                color = (button["color"][0], button["color"][1], button["color"][2])
                btnrect = pg.Rect(w/4 + 30 * colcount * spread_x * size_multiplier + offset_btn_x, 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y, 86 * size_multiplier * bw, 86 * size_multiplier)
                if btnrect.collidepoint(pg.mouse.get_pos()):
                    c2 = ()
                    for i in color:
                        if i > 50:
                            i -= 50
                        c2 += (i,)
                    color = c2
                txtcolor = (0, 0, 0)

                '''if "addorder" in button["buttontype"]:
                    txtcolor = (255, 255, 255)
                    if "item" in button["itemtype"] or "menu" in button["itemtype"]:
                        pg.draw.rect(screen, color, (w/4 + 30 * colcount * spread_x * size_multiplier + offset_btn_x, 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y, 86 * size_multiplier, 86 * size_multiplier), 2, border_radius=15)
                    elif "drink" in button["itemtype"]:
                        pg.draw.circle(screen, color, (w/4 + 30 * colcount * spread_x * size_multiplier + offset_btn_x + (43 * size_multiplier), 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y + (43 * size_multiplier)), 43 * size_multiplier, 2)
                elif button["buttontype"] == "manage":
                    if button["action"] == "deleteorder":
                        pg.draw.rect(screen, color, (w/4 + 30 * colcount * spread_x * size_multiplier + offset_btn_x, 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y, 86 * size_multiplier, 86 * size_multiplier), border_radius=15)
                    else:
                        pg.draw.rect(screen, color, (w/4 + 30 * colcount * spread_x * size_multiplier + offset_btn_x, 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y, 86 * size_multiplier, 86 * size_multiplier), 2, border_radius=15)
                        txtcolor = (255, 50, 50)
                elif button["buttontype"] == "switchview":
                    pg.draw.rect(screen, color, (w/4 + 30 * colcount * spread_x * size_multiplier + offset_btn_x, 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y, 86 * size_multiplier, 86 * size_multiplier), border_radius=15)
                elif button["buttontype"] == "modifyitem":
                    pg.draw.rect(screen, color, (w/4 + 30 * colcount * spread_x * size_multiplier + offset_btn_x, 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y, 86 * size_multiplier, 86 * size_multiplier), border_radius=30)
                elif button["buttontype"] == "action":
                    pg.draw.rect(screen, color, (w/4 + 30 * colcount * spread_x * size_multiplier + offset_btn_x, 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y, 86 * size_multiplier * bw, 86 * size_multiplier), border_radius=15)
                '''

                fill = button["fill"]
                if fill:
                    txtcolor = (0, 0, 0)
                else:
                    txtcolor = color
                shape = button["shape"]
                if "rect" in shape:
                    if "rounded" in shape:
                        if fill:
                            pg.draw.rect(screen, color, btnrect, border_radius=30)
                        else:
                            pg.draw.rect(screen, color, btnrect, 2, border_radius=30)
                    else:
                        if fill:
                            pg.draw.rect(screen, color, btnrect, border_radius=15)
                        else:
                            pg.draw.rect(screen, color, btnrect, 2, border_radius=15)
                elif "round" in shape:
                    if fill:
                        pg.draw.circle(screen, color, btnrect.center, 43 * size_multiplier)
                    else:
                        pg.draw.circle(screen, color, btnrect.center, 43 * size_multiplier, 2)


                try:
                    buttontext = button["text"].split(" ")
                    txtlen = int(round((len(buttontext[0]) + len(buttontext[1])) / 2, 1))
                except:
                    txtlen = len(button["text"])

                fontsize = int((28 - txtlen - 5) * bw * size_multiplier)
                btnfont = pg.font.Font("assets/fonts/sysfont_bold.ttf", fontsize)

                if type(buttontext) == list and len(buttontext) >= 2:
                    text1 = btnfont.render(buttontext[0], True, txtcolor)
                    text2 = btnfont.render(buttontext[1], True, txtcolor)
                    if len(buttontext) == 3:
                        text3 = btnfont.render(buttontext[2], True, txtcolor)
                        screen.blit(text1, text1.get_rect(center=(btnrect.center[0], 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y + offset_txt_y + 40-(20 * size_multiplier))))
                        screen.blit(text2, text2.get_rect(center=(btnrect.center[0], 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y + offset_txt_y + 40)))
                        screen.blit(text3, text3.get_rect(center=(btnrect.center[0], 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y + offset_txt_y + 40+(20 * size_multiplier))))
                    else:
                        screen.blit(text1, text1.get_rect(center=(btnrect.center[0], 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y + offset_txt_y + 40-(10 * size_multiplier))))
                        screen.blit(text2, text2.get_rect(center=(btnrect.center[0], 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y + offset_txt_y + 40+(10 * size_multiplier))))
                else:
                    text = btnfont.render(button["text"], True, txtcolor)
                    screen.blit(text, text.get_rect(center=(btnrect.center[0], 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y + offset_txt_y + 43)))
                
            colcount += 1
        colcount = 0
        rowcount += 1

def draw_pmenu():
    global pay, neworder, order, paycompletedelay, pay_complete, keypad_mul, button_sizing
    offsx, offsy, mulx, muly, size, = keypad_mul
    bw_double, bw_triple, bw_quadruple = button_sizing
    rowcount = 0
    colcount = 0
    buttons = paymenu

    draw_neworder()

    if order.paid < order.get_price():
        pg.draw.rect(surface, (200, 200, 200), (w/4+40, 170, w/4+50, h-240), 3, border_radius=15)
        pg.draw.rect(surface, (255, 255, 255), (w/4+90, 170, w/4-50, 220), border_radius=15)

        for row in buttons:
            for button in row:
                #button box
                try:
                    if button["buttonsize"] == "double":
                        bw = bw_double
                        tw = 2.4
                        fs = 2.4
                    elif button["buttonsize"] == "triple":
                        bw = bw_triple
                        tw = 3.4
                        fs = 3.4
                    elif button["buttonsize"] == "quadruple":
                        bw = bw_quadruple
                        tw = 5.5
                        fs = 2.5
                except:
                    bw = 1
                    tw = 1
                    fs = 1
                    pass
                if button["buttontype"] == "blank":
                    pass
                else:
                    btnrect = pg.Rect(w/4 + 30 * colcount * spread_x * size_multiplier + offset_btn_x, 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y, 86 * size_multiplier * bw, 86 * size_multiplier)
                    if btnrect.collidepoint(pg.mouse.get_pos()):
                        color = (200, 200, 200)
                    else:
                        color = (button["color"][0], button["color"][1], button["color"][2])
                    txtcolor = (0, 0, 0)
                    transparent = False
                    try:
                        if button["color"][3] == 1:
                            color = (color[0], color[1], color[2])
                            transparent = True
                    except:
                        pass
                    
                    if transparent:
                        pg.draw.rect(screen, color, btnrect, 2, border_radius=15)
                        txtcolor = (255, 255, 255)
                    else:
                        if color == (255, 255, 255):
                            txtcolor = (0, 0, 0)
                        pg.draw.rect(screen, color, btnrect, border_radius=15)

                    if button["buttontype"] == "manage" and button["action"] == "back":
                        txtcolor = (255, 50, 50)

                    try:
                        buttontext = button["text"].split(" ")
                        txtlen = int(round((len(buttontext[0]) + len(buttontext[1])) / 2, 1))
                    except:
                        txtlen = len(button["text"])

                    fontsize = int((28 - txtlen - 5) * fs * size_multiplier)
                    btnfont = pg.font.Font("assets/fonts/sysfont_bold.ttf", fontsize)

                    if type(buttontext) == list and len(buttontext) >= 2:
                        text1 = btnfont.render(buttontext[0], True, txtcolor)
                        text2 = btnfont.render(buttontext[1], True, txtcolor)
                        if len(buttontext) == 3:
                            text3 = btnfont.render(buttontext[2], True, txtcolor)
                            screen.blit(text1, text1.get_rect(center=(btnrect.center[0], 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y + offset_txt_y + 40-(20 * size_multiplier))))
                            screen.blit(text2, text2.get_rect(center=(btnrect.center[0], 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y + offset_txt_y + 40)))
                            screen.blit(text3, text3.get_rect(center=(btnrect.center[0], 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y + offset_txt_y + 40+(20 * size_multiplier))))
                        else:
                            screen.blit(text1, text1.get_rect(center=(btnrect.center[0], 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y + offset_txt_y + 40-(10 * size_multiplier * (fs / 1.3)))))
                            screen.blit(text2, text2.get_rect(center=(btnrect.center[0], 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y + offset_txt_y + 40+(10 * size_multiplier * (fs / 1.3)))))
                    else:
                        text = btnfont.render(button["text"], True, txtcolor)
                        screen.blit(text, text.get_rect(center=(btnrect.center[0], 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y + offset_txt_y + 43)))
                    
                colcount += 1
            colcount = 0
            rowcount += 1

        screen.blit(smallfont_bold.render("Fizetendő:", True, (0, 0, 0)), (w/4+100, 190))
        screen.blit(titlefont_bold.render(f"{order.get_price()-order.paid} Ft", True, (0, 0, 0)), (w/4+100, 200))
        screen.blit(smallfont_bold.render("Fizetett:", True, (0, 0, 0)), (w/4+100, 270))
        if add_count != "0":
            paid = add_count
        else:
            paid = order.paid
        screen.blit(titlefont_bold.render(f"{paid} Ft", True, (0, 0, 0)), (w/4+100, 280))

        cnt = 0
        for y in range(4):
            for x in range(3):
                cnt += 1
                rect = pg.Rect(w/4+offsx+(90*mulx*((x*1.4)+1)), 380+offsy+90*muly*((y*1.4)+1), ((w/4-50)/3-10)*size, ((w/4-50)/3-10)*size)
                if rect.collidepoint(pg.mouse.get_pos()):
                    color = (225, 225, 225)
                else:
                    color = (255, 255, 255)
                pg.draw.rect(surface, color, rect, border_radius=15)
                text = cnt
                if cnt == 10:
                    text = "C"
                elif cnt == 11:
                    text = 0
                elif cnt == 12:
                    text = "#"
                text = titlefont_bold.render(str(text), True, (0, 0, 0))
                screen.blit(text, text.get_rect(center=(rect.center)))

    elif order.paid >= order.get_price():
        if order.paid > order.get_price():
            pg.draw.rect(surface, (255, 255, 255), (w/4+90, 170, w/4-50, 300), border_radius=15)
            screen.blit(smallfont_bold.render("Viszzajár:", True, (0, 0, 0)), (w/4+100, 350))
            screen.blit(titlefont_bold.render(f"{order.paid - order.get_price()} Ft", True, (0, 0, 0)), (w/4+100, 360))
        elif order.paid == order.get_price():
            pg.draw.rect(surface, (255, 255, 255), (w/4+90, 170, w/4-50, 220), border_radius=15)
        screen.blit(smallfont_bold.render("Fizetendő:", True, (0, 0, 0)), (w/4+100, 190))
        required = order.get_price()-order.paid
        if required < 0:
            required = 0
        screen.blit(titlefont_bold.render(f"{required} Ft", True, (0, 0, 0)), (w/4+100, 200))
        screen.blit(smallfont_bold.render("Fizetett:", True, (0, 0, 0)), (w/4+100, 270))
        screen.blit(titlefont_bold.render(f"{order.paid} Ft", True, (0, 0, 0)), (w/4+100, 280))

        if not order.complete:
            order.complete = True
            makeReceipt(order)
            pay = False
            pay_complete = time.time()
            paycompletedelay = True

    if not pay:
        if time.time() - pay_complete > 10:
            paycompletedelay = False

            orders.remove(orders[0])
            orders_complete.append(order)
            neworder = False
            order = None
        else:
            pg.draw.rect(screen, (255, 255, 255), (w/2+100, 170, w/2-200, h-250), 5, border_radius=15)
            screen.blit(titlefont_bold.render(f"{int(abs((time.time() - pay_complete)-10))}", True, (255, 255, 255)), (w/2+w/4, h/2+200))
            screen.blit(titlefont.render("Rendelés vége", True, (255, 255, 255)), (w/4+100, h/2))
            screen.blit(titlefont.render("A rendelés lezárult.", True, (255, 255, 255)), (w/2+130, 180))
            text = "Folytassa a kasszagépkezelési protokollt, \na kasszát ne hagyja el ha nincs bezárva.\n\nBankkártyás fizetés esetén végezze el a\nbankkártyaterminálon a szükséges lépéseket.\n\nA rendszer automatikusan visszalép ha az idő\nletelik."
            for line in text.split("\n"):
                linenum = text.split("\n").index(line)+1
                screen.blit(font.render(line, True, (255, 255, 255)), (w/2+130, 270 + 30*linenum))
        
def click_pmenu_keypad():
    global cnt, order, add_count, keypad_mul
    offsx, offsy, mulx, muly, size = keypad_mul
    cnt = 0
    for y in range(4):
        for x in range(3):
            cnt += 1
            rect = pg.Rect(w/4+offsx+(90*mulx*((x*1.4)+1)), 380+offsy+90*muly*((y*1.4)+1), ((w/4-50)/3-10)*size, ((w/4-50)/3-10)*size)
            if rect.collidepoint(pg.mouse.get_pos()):
                if cnt <= 9:
                    if add_count == "0":
                        add_count = str(cnt)
                    else:
                        add_count += str(cnt)
                elif cnt == 10:
                    add_count = "0"
                elif cnt == 11:
                    if add_count == "0":
                        add_count = "0"
                    else:
                        add_count += "0"
                elif cnt == 12:
                    order.paid += int(add_count)
                    add_count = "0"

def click_pmenu():
    global pay, neworder, button_sizing
    bw_double, bw_triple, bw_quadruple = button_sizing

    rowcount = 0
    colcount = 0
    buttons = paymenu

    for row in buttons:
        for button in row:
            #button box
            try:
                if button["buttonsize"] == "double":
                    bw = bw_double
                    tw = 2.4
                    fs = 2.4
                elif button["buttonsize"] == "triple":
                    bw = bw_triple
                    tw = 3.4
                    fs = 3.4
                elif button["buttonsize"] == "quadruple":
                    bw = bw_quadruple
                    tw = 5.5
                    fs = 2.5
            except:
                bw = 1
                tw = 1
                fs = 1
                pass
            if button["buttontype"] == "blank":
                pass
            else:
                if pg.Rect(w/4 + 30 * colcount * spread_x * size_multiplier + offset_btn_x, 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y, 86 * size_multiplier * bw, 86 * size_multiplier).collidepoint(pg.mouse.get_pos()):
                    if button["buttontype"] == "payamount" and not button["action"] == "exact":
                        payadd = button["action"]
                        try:
                            payadd.replace(".", "")
                        except:
                            pass
                        if order.paid < order.get_price():
                            order.paid += int(payadd)
                    elif button["buttontype"] == "payamount" and button["action"] == "exact" and not order.paid >= order.get_price():
                        order.paid = order.get_price()
                    elif button["buttontype"] == "manage":
                        if button["action"] == "back":
                            if order.paid == 0:
                                pay = False
                                orders.remove(orders[0])
                                neworder = True
                                for item in order.items:
                                    if item["type"] == "discount":
                                        order.items.remove(item)
                            else:
                                popups["uneditable"].active = True
                        elif button["action"] == "adminmenu":
                            global settings
                            settings = True
                    elif button["buttontype"] == "action" and button["action"] == "discount":
                        found = False
                        for item in order.items:
                            if item["type"] == "discount":
                                found = True
                                break
                        if order.paid == 0 and not found:
                            order.items.append({"name": "20% Kedvezmény",
                                                "type": "discount",
                                                "price": -order.get_price()*0.2,
                                                "count": 1
                                                })
                        elif order.paid == 0 and found:
                            popups["discountfound"].active = True
                        elif order.paid > 0:
                            popups["uneditable"].active = True
                    elif button["buttontype"] == "action" and button["action"] == "card":
                        order.paid = order.get_price()
                        order.paymentmethod = "Kártya"
                    
            colcount += 1
        colcount = 0
        rowcount += 1

    if order.paid < order.get_price():
        click_pmenu_keypad()

def click_if():
    global newmenu, pay, selected, order, switch_view, item_count, addsize, neworder, orders_complete, button_sizing
    bw_double, bw_triple, bw_quadruple = button_sizing
    if addsize == "M-":
        pricemultiplier = 0.8
    elif addsize == "M":
        pricemultiplier = 1
    elif addsize == "M+":
        pricemultiplier = 1.4
    else:
        pricemultiplier = 1
    if pg.Rect(w/4+10, 80, w-w/4-50, h-100).collidepoint(pg.mouse.get_pos()):
        rowcount = 0
        colcount = 0
        buttons = interface[switch_view]

        for row in buttons:
            for button in row:
                try:
                    if button["buttonsize"] == "double":
                        bw = bw_double
                        tw = 2.4
                        fs = 2.4
                    elif button["buttonsize"] == "triple":
                        bw = bw_triple
                        tw = 3.4
                        fs = 3.4
                    elif button["buttonsize"] == "quadruple":
                        bw = bw_quadruple
                        tw = 5.5
                        fs = 2.5
                except:
                    bw = 1
                    tw = 1
                    fs = 1
                    pass
                if pg.Rect(w/4 + 30 * colcount * spread_x * size_multiplier + offset_btn_x, 50 + 30 * rowcount * spread_y * size_multiplier + offset_btn_y, 86 * size_multiplier * bw, 86 * size_multiplier).collidepoint(pg.mouse.get_pos()) and button["buttontype"] != "blank":
                    print(button["text"])
                    if button["buttontype"] == "addorder":
                        try:
                            if "sizeable" in button["property"]:
                                itemname = button["itemname"] + " " + addsize
                            else:
                                itemname = button["itemname"]
                                pricemultiplier = 1
                        except:
                            itemname = button["itemname"]
                            pricemultiplier = 1
                        if "item" in button["itemtype"] and newmenu == None:
                            if order == None:
                                order = Order(len(orders_complete), datetime.now(), [])
                            in_order = False
                            for item in order.items:
                                if item["name"] == itemname:
                                    in_order = True
                                    item["count"] += item_count
                            if not in_order:
                                order.items.append({"name": itemname,
                                                    "type": "item",
                                                    "price": button["price"] * pricemultiplier,
                                                    "count": item_count
                                                    })
                        elif button["itemtype"] == "menu":
                            if order == None:
                                order = Order(len(orders_complete), datetime.now(), [])
                            newmenu = Menu(itemname, [], button["price"] * pricemultiplier, item_count)
                            print("new menu created")
                        
                        elif "drink" in button["itemtype"] and type(newmenu) == Menu:
                            found = False
                            for item in newmenu.items:
                                if "drink" in item["type"]:
                                    found = True

                            if not found:
                                newmenu.items.append({"name": button["itemname"],
                                                    "type": "drink",
                                                    "price": button["price"],
                                                    "count": newmenu.qty
                                                    })
                                
                        elif "koret" in button["itemtype"] and type(newmenu) == Menu:
                            found = False   
                            for item in newmenu.items:
                                if "koret" in item["type"]:
                                    found = True
                            
                            if not found:
                                newmenu.items.append({"name": button["itemname"],
                                                    "type": "koret",
                                                    "price": button["price"],
                                                    "count": newmenu.qty
                                                    })
                        addsize = "M"
                        item_count = 1
                            
                    elif button["buttontype"] == "manage":
                        global settings, settings_property
                        if button["action"] == "deleteorder":
                            order = None
                        if button["action"] == "deleteitem" and selected != None:
                            order.items.remove(order.items[selected[1]])
                            selected = None
                        if button["action"] == "deletemenuitem":
                            if order.items[selected[1]]["type"] == "menu":
                                menu = order.items[selected[1]]
                                order.items.remove(order.items[selected[1]])
                                newmenu = Menu(menu["name"], [], menu["price"], menu["count"])
                        if button["action"] == "setdisplaysize":
                            settings = True
                            settings_property = "setdisplaysize"
                            switch_view = next(iter(interface))
                        if button["action"] == "setbuttonpos":
                            settings = True
                            settings_property = "setbuttonpos"
                            switch_view = next(iter(interface))
                    elif button["buttontype"] == "switchview":
                        switch_view = button["switchview"]
                    elif button["buttontype"] == "modifyitem":
                        if button["action"] == "small":
                            addsize = "M-"
                        elif button["action"] == "medium":
                            addsize = "M"
                        elif button["action"] == "large":
                            addsize = "M+"
                    elif button["buttontype"] == "action":
                        if button["action"] == "pay":
                            if order != None:
                                if len(order.items) > 0:
                                    pay = True
                                    orders.append(order)
                                else:
                                    popups["noorder"].active = True
                            else:
                                popups["noorder"].active = True

                        if button["action"] == "back":
                            if order != None:
                                if len(order.items) > 0:
                                    popups["unfinishedorder"].active = True
                                else:
                                    neworder = False
                                    order = None
                            elif order == None:
                                neworder = False
                                order = None

                colcount += 1
            colcount = 0
            rowcount += 1
        return None, order, switch_view, addsize, item_count
    elif pg.Rect(30, 80, w/4-50, h-100).collidepoint(pg.mouse.get_pos()) and order != None:
        found = False
        space = 0
        for item in order.items:
            if pg.Rect(40, 175 + (order.items.index(item) + space) * 30, w/4-50, 35).collidepoint(pg.mouse.get_pos()):
                selected = [order.items.index(item) + space, order.items.index(item)]
                found = True
            if item["type"] == "menu":
                space += 2
        if not found:
            selected = None
        return selected, order, switch_view, addsize, item_count
    else:
        return None, order, switch_view, addsize, item_count
    
def draw_neworder():
    global newmenu
    y = 70
    if selected != None:
        pg.draw.rect(surface, (255, 255, 255), (30, 102 + selected[0] * 30 + y, w/4-50, 35), 2, border_radius=5)
    if order != None:
        space = 0
        for i in range(len(order.items)):
            name = order.items[i]["name"]
            qty = order.items[i]["count"]
            price = int(order.items[i]["price"] * qty)
            screen.blit(neworderfont.render(f"{qty} {name}", True, (255, 255, 255)), (40, 100 + i + space * 30 + y))
            screen.blit(neworderfont.render(f"{price} Ft", True, (255, 255, 255)), (w/4-(neworderfont.render(f"{price} Ft", True, fontcolor).get_width()) - 30, 100 + i + space * 30 + y))
            try:
                if order.items[i]["type"] == "menu":
                    for item in order.items[i]["items"]:
                        space += 1
                        screen.blit(neworderfont.render(f"{item['name']}", True, (255, 255, 255)), (80, 100 + i + space * 30 + y))
                space += 1
            except:
                pass
        if newmenu != None:
            print("newmenu drawing")
            screen.blit(neworderfont.render(newmenu.name, True, (255, 255, 255)), (40, 100 + len(order.items) + space * 30 + y))
            screen.blit(neworderfont.render(f"{newmenu.price} Ft", True, (255, 255, 255)), (w/4-(neworderfont.render(f"{newmenu.price} Ft", True, fontcolor).get_width()) - 30, 100 + len(order.items) + space * 30 + y))
            found_drink = False
            found_koret = False
            for item in newmenu.items: 
                if item["type"] == "drink":
                    found_drink = True
                if item["type"] == "koret":
                    found_koret = True
            if found_drink:
                screen.blit(neworderfont.render(f"{item['name']}", True, (255, 255, 255)), (80, 100 + (len(order.items) + 1) + (space + 1) * 30 + y))
            else:
                screen.blit(neworderfont.render("Válassz üdítőt!", True, (255, 50, 50)), (80, 100 + (len(order.items) + 1) + (space + 1) * 30 + y))
            if found_koret:
                screen.blit(neworderfont.render(f"{item['name']}", True, (255, 255, 255)), (80, 100 + (len(order.items) + 2) + (space + 2) * 30 + y))
            else:
                screen.blit(neworderfont.render("Válassz köretet!", True, (255, 50, 50)), (80, 100 + (len(order.items) + 2) + (space + 2) * 30 + y))         

            if found_drink and found_koret:
                order.items.append({"name": newmenu.name,
                                    "type": "menu",
                                    "price": newmenu.price,
                                    "count": newmenu.qty,
                                    "items": newmenu.items
                                    })
                newmenu = None

pg.init()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
surface = pg.display.get_surface()
w, h = size = surface.get_width(), surface.get_height()
pg.display.set_caption("VajkyPOS")
clock = pg.time.Clock()

preload_font = pg.font.Font("assets/fonts/sysfont.ttf", 30)
load_interface = preload_font.render("Interfész fájlok beolvasása", True, (255, 255, 255))
load_fonts = preload_font.render("Betűtípusok betöltése", True, (255, 255, 255))
load_images = preload_font.render("Ikonok betöltése", True, (255, 255, 255))
load_etc = preload_font.render("Máris megvagyunk...", True, (255, 255, 255))


offset_btn_x = 50
offset_txt_x = 0
spread_x = 3.8
offset_btn_y = 60
offset_txt_y = 0
spread_y = 3.8

progressbar = 0
fontcolor = (255, 255, 255)

def loadbar_update():
    global progressbar, loaditems, incr
    progressbar += incr
    screen.fill((0, 0, 0))
    if progressbar < 25:
        screen.blit(load_interface, load_interface.get_rect(center=(w/2, h-150)))
    elif progressbar < 50:
        screen.blit(load_fonts, load_fonts.get_rect(center=(w/2, h-150)))
    elif progressbar < 75:
        screen.blit(load_images, load_images.get_rect(center=(w/2, h-150)))
    else:
        screen.blit(load_etc, load_etc.get_rect(center=(w/2, h-150)))
    screen.blit(logo, logo.get_rect(center=(w/2, h/2)))
    pg.draw.rect(surface, (100, 100, 100), (w/4, h-100, w/2, 11), border_radius=5)
    pg.draw.rect(surface, (255, 255, 255), (w/4, h-99, (w/2) * (progressbar / 100), 10), border_radius=5)
    pg.draw.rect(surface, (255, 255, 255), (w/4, h-99, (w/2) * (progressbar / 100), 10), border_radius=5)
    pg.display.flip()

loaditems = 17
incr = 100 / loaditems

logo = pg.image.load("assets/img/logo.png")
logo_small = pg.transform.scale(logo, (300, 150))
loadbar_update()
try:
    with open("interface/settings.json", "r", encoding="utf-8") as file:
        loaded = load(file)
        offsets = loaded["offsets"]
        fontsizes = loaded["fontsize"]
        offset_btn_x = offsets["offset_btn_x"]
        offset_txt_x = offsets["offset_txt_x"]
        spread_x = offsets["spread_x"]
        offset_btn_y = offsets["offset_btn_y"]
        offset_txt_y = offsets["offset_txt_y"]
        spread_y = offsets["spread_y"]
        size_multiplier = offsets["size_multiplier"]
        keypad_mul = offsets["keypad_mul"][0], offsets["keypad_mul"][1], offsets["keypad_mul"][2], offsets["keypad_mul"][3], offsets["keypad_mul"][4],
        button_sizing = offsets["button_sizing"][0], offsets["button_sizing"][1], offsets["button_sizing"][2]
        
        smallfont_size = fontsizes["smallfont"]
        font_size = fontsizes["font"]
        titlefont_size = fontsizes["titlefont"]
        neworderfont_size = fontsizes["neworderfont"]

        preset = loaded["preset"]
except Exception as e:
    print("Hiba a beállítások betöltése közben!")
    error("load-interface", "002", "settings.json", e)
loadbar_update()
try:
    with open("interface/presets.json", "r", encoding="utf-8") as file:
        presets = load(file)
except Exception as e:
    print("Hiba a beállítások betöltése közben!")
    error("load-presets", "004", "presets.json", e)
loadbar_update()
try:
    with open("orders.json", "r", encoding="utf-8") as save:
        orders_loaded = load(save)
except:
    orders_loaded = {"orders":[]}
    with open("orders.json", "w", encoding="utf-8") as save:
        dump(orders_loaded, save)
try:
    with open("interface/neworder.json", "r", encoding="utf-8") as file:
        interface = load(file)
except Exception as e:
    print("Hiba az interfész betöltése közben!")
    error("load-interface", "001", "neworder.json", e)
loadbar_update()
try:
    smallfont = pg.font.Font("assets/fonts/sysfont.ttf", smallfont_size)
    font = pg.font.Font("assets/fonts/sysfont.ttf", font_size)
    titlefont = pg.font.Font("assets/fonts/sysfont.ttf", titlefont_size)
    neworderfont = pg.font.Font("assets/fonts/sysfont.ttf", neworderfont_size)
    loadbar_update()
    smallfont_bold = pg.font.Font("assets/fonts/sysfont_bold.ttf", smallfont_size)
    font_bold = pg.font.Font("assets/fonts/sysfont_bold.ttf", font_size)
    font_extrabold = pg.font.Font("assets/fonts/sysfont_extrabold.ttf", font_size)
    titlefont_bold = pg.font.Font("assets/fonts/sysfont_bold.ttf", titlefont_size)
    titlefont_extrabold = pg.font.Font("assets/fonts/sysfont_extrabold.ttf", titlefont_size)
    loadbar_update()
    font_bolditalic = pg.font.Font("assets/fonts/sysfont_bolditalic.ttf", font_size)
    titlefont_bolditalic = pg.font.Font("assets/fonts/sysfont_bolditalic.ttf", titlefont_size)
    loadbar_update()
    font_light = pg.font.Font("assets/fonts/sysfont_light.ttf", font_size)
    titlefont_light = pg.font.Font("assets/fonts/sysfont_light.ttf", titlefont_size)
    loadbar_update()
except Exception as e:
    print("Hiba a betűtípusok betöltése közben!")
    error("load-fonts", "003", "n/a", e)
try:
    personicon = pg.image.load("assets/img/personicon.png")
    personicon = pg.transform.scale(personicon, (50, 50))
    loadbar_update()
    clockicon = pg.image.load("assets/img/clockicon.png")
    clockicon = pg.transform.scale(clockicon, (50, 50))
    loadbar_update()
    cancelicon = pg.image.load("assets/img/cancel.png")
    cancelicon_sm = pg.transform.scale(cancelicon, (50, 50))
    loadbar_update()
    continueicon = pg.image.load("assets/img/continueicon.png")
    loadbar_update()
    erroricon = pg.image.load("assets/img/erroricon.png")
    loadbar_update()
    warnicon = pg.image.load("assets/img/warnicon.png")
    warnicon = pg.transform.scale(warnicon, (180, 180))
    loadbar_update()
except Exception as e:
    print("Hiba az ikonok betöltése közben!")
    error("load-images", "003", "n/a", e)
no_order_text = titlefont_bold.render("Jelenleg nincs rendelés", True, fontcolor)
no_order_subtitle = font.render("Koppintson a rendelés felvételéhez", True, fontcolor)
loadbar_update()

class Order:
    def __init__(self, num, time, items):
        self.num = num
        self.time = time
        self.items = items
        self.paid = 0
        self.complete = False
        self.paymentmethod = "Készpénz"

    def get_time(self):
        return datetime.datetime.now() - self.time
    
    def get_price(self):
        price = 0
        for item in self.items:
            price += item["price"] * item["count"]
        return price
    
    def status(self):
        if self.paid >= self.get_price():
            self.status = "complete"
        elif self.paid > 0:
            self.status = "half-paid"
        elif self.paid == 0:
            self.status = "pending"
    
class Menu:
    def __init__(self, name, items, price, qty):
        self.name = name
        self.items = items
        self.price = price
        self.qty = qty

class Popup:
    def __init__(self, type, title, text, active=False):
        self.type = type
        self.title = titlefont.render(title, True, (0, 0, 0))
        self.text = font.render(text, True, (0, 0, 0))
        self.active = active
        self.width = self.text.get_width()+50
        self.height = 200
        self.btn_rect = pg.Rect(w/2-50, h/2-101+self.height-50, 200, 40)

    def draw(self):
        if self.active:
            pg.draw.rect(screen, (0, 0, 0), (w/2-501, h/2-101, 1002, 202), border_radius=40)
            pg.draw.rect(screen, (225, 225, 225), (w/2-500, h/2-100, 1000, 200), border_radius=40)
            screen.blit(self.title, (w/2-250, h/2-80))
            screen.blit(self.text, (w/2-240, h/2-10))
            pg.draw.rect(screen, (255, 0, 0), self.btn_rect, border_radius=10)
            ok = font.render("OK", True, (255, 255, 255))
            screen.blit(ok, ok.get_rect(center=(self.btn_rect.x+self.btn_rect.width/2, self.btn_rect.y+self.btn_rect.height/2)))
            if self.type == "warn":
                screen.blit(warnicon, warnicon.get_rect(center=(w/2-380, h/2)))
            elif self.type == "alert":
                pass
            elif self.type == "error":
                pass
    
    def click(self):
        if self.btn_rect.collidepoint(pg.mouse.get_pos()):
            self.active = False
        
    @classmethod
    def isActive(cls):
        for popup in popups:
            if popups[popup].active == True:
                return True
        return False


#variable declarations
orders = []
orders_complete = []
pay = False
neworder = False
selected = None
switch_view = "buttons"
settings = False
num = 1
addnum = 0
item_count = 1
addsize = "M"
quit_confirm = False
paycompletedelay = False
add_count = "0"
username = "Vajk Ádám"
settings_property = "setbuttonpos"

paymenu = [
    [
        {
            "buttontype":"blank"
        },
        {
            "buttontype":"blank"
        },
        {
            "buttontype":"blank"
        },
        {
            "text":"Kártyás fizetés",
            "buttontype":"action",
            "action":"card",
            "color":(255, 255, 255)
        },
        {
            "text":"20% kedvezm.",
            "buttontype":"action",
            "action":"discount",
            "color":(255, 255, 255)
        },
        {
            "text":"Admin menü",
            "buttontype":"manage",
            "action":"adminmenu",
            "color":(255, 255, 255)
        },
        {
            "text":"Rendelés módosítása",
            "buttontype":"manage",
            "action":"back",
            "color":(255, 0, 0, 1)
        }
    ],
    [
        {
            "buttontype":"blank"
        },
        {
            "buttontype":"blank"
        },
        {
            "buttontype":"blank"
        },
        {
            "text":"PONTOS ÖSSZEG",
            "buttontype":"payamount",
            "action":"exact",
            "color":(255, 255, 255),
            "buttonsize":"quadruple"
        }
    ],
    [
        {
            "buttontype":"blank"
        },
        {
            "buttontype":"blank"
        },
        {
            "buttontype":"blank"
        },
        {
            "text":"10.000",
            "buttontype":"payamount",
            "action":10000,
            "buttonsize":"double",
            "color":(255, 255, 255)
        },
        {
            "buttontype":"blank"
        },
        {
            "text":"20.000",
            "buttontype":"payamount",
            "action":20000,
            "buttonsize":"double",
            "color":(255, 255, 255)
        }
    ],
    [
        {
            "buttontype":"blank"
        },
        {
            "buttontype":"blank"
        },
        {
            "buttontype":"blank"
        },
        {
            "text":"2000",
            "buttontype":"payamount",
            "action":2000,
            "buttonsize":"double",
            "color":(255, 255, 255)
        },
        {
            "buttontype":"blank"
        },
        {
            "text":"5000",
            "buttontype":"payamount",
            "action":5000,
            "buttonsize":"double",
            "color":(255, 255, 255)
        }
    ],
    [
        {
            "buttontype":"blank"
        },
        {
            "buttontype":"blank"
        },
        {
            "buttontype":"blank"
        },
        {
            "text":"500",
            "buttontype":"payamount",
            "action":500,
            "buttonsize":"double",
            "color":(255, 255, 255)
        },
        {
            "buttontype":"blank"
        },
        {
            "text":"1000",
            "buttontype":"payamount",
            "action":1000,
            "buttonsize":"double",
            "color":(255, 255, 255)
        }
    ]
]

quit_confirm_confirm = pg.Rect(w/2, h/2+40, 200, 50)
quit_confirm_cancel = pg.Rect(w/2-240, h/2+40, 200, 50)

plus = font.render("+", True, (0, 0, 0))
minus = font.render("-", True, (0, 0, 0))
sizemultiplierplus_rect = plus.get_rect(topleft=(w/2+250, h/2-60))
sizemultiplierminus_rect = minus.get_rect(topleft=(w/2+150, h/2-60))
buttonsoffsetxplus_rect = plus.get_rect(topleft=(w/2+250, h/2-30))
buttonsoffsetxminus_rect = minus.get_rect(topleft=(w/2+150, h/2-30))
buttonsoffsetyplus_rect = plus.get_rect(topleft=(w/2+250, h/2))
buttonsoffsetyminus_rect = minus.get_rect(topleft=(w/2+150, h/2))
textoffsetxplus_rect = plus.get_rect(topleft=(w/2+250, h/2+30))
textoffsetxminus_rect = minus.get_rect(topleft=(w/2+150, h/2+30))
textoffsetyplus_rect = plus.get_rect(topleft=(w/2+250, h/2+60))
textoffsetyminus_rect = minus.get_rect(topleft=(w/2+150, h/2+60))
spreadoffsetxplus_rect = plus.get_rect(topleft=(w/2+250, h/2+90))
spreadoffsetxminus_rect = minus.get_rect(topleft=(w/2+150, h/2+90))
spreadoffsetyplus_rect = plus.get_rect(topleft=(w/2+250, h/2+120))
spreadoffsetyminus_rect = minus.get_rect(topleft=(w/2+150, h/2+120))
smallfonttextplus_rect = plus.get_rect(topleft=(w/2+250, h/2-180))
smallfonttextminus_rect = minus.get_rect(topleft=(w/2+150, h/2-180))
fontsizetextplus_rect = plus.get_rect(topleft=(w/2+250, h/2-150))
fontsizetextminus_rect = minus.get_rect(topleft=(w/2+150, h/2-150))
titlefontsizetextplus_rect = plus.get_rect(topleft=(w/2+250, h/2-120))
titlefontsizetextminus_rect = minus.get_rect(topleft=(w/2+150, h/2-120))
neworderfontsizetextplus_rect = plus.get_rect(topleft=(w/2+250, h/2-90))
neworderfontsizetextminus_rect = minus.get_rect(topleft=(w/2+150, h/2-90))

sizemultipliervaltext = font.render(str(size_multiplier), True, (0, 0, 0))
buttonsoffsetxvaltext = font.render(str(offset_btn_x), True, (0, 0, 0))
buttonsoffsetyvaltext = font.render(str(offset_btn_y), True, (0, 0, 0))
textoffsetxvaltext = font.render(str(offset_txt_x), True, (0, 0, 0))
textoffsetyvaltext = font.render(str(offset_txt_y), True, (0, 0, 0))
spreadoffsetxvaltext = font.render(str(spread_x), True, (0, 0, 0))
spreadoffsetyvaltext = font.render(str(spread_y), True, (0, 0, 0))
smallfontvaltext = font.render(str(smallfont_size), True, (0, 0, 0))
fontvaltext = font.render(str(font_size), True, (0, 0, 0))
titlefontvaltext = font.render(str(titlefont_size), True, (0, 0, 0))
neworderfontvaltext = font.render(str(neworderfont_size), True, (0, 0, 0))

popups = {
    "uneditable": Popup("warn", "Figyelem!", "A rendelés nem módosítható", False),
    "generalerr": Popup("warn", "Hiba!", "A művelet nem végrehajtható!", False),
    "discountfound": Popup("warn", "Kedvezmény hiba!", "A kedvezmény egyszer már érvényesítve lett", False),
    "unfinishedorder": Popup("warn", "Befejezetlen rendelés!", "A rendelést be kell fejezni a művelet végrehajtásához!", False),
    "noorder": Popup("warn", "Nincs rendelés!", "A művelet végrehajtásához vegye fel a rendelést!")
}

mainloop = True
while mainloop:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit_confirm = True
        if event.type == pg.MOUSEBUTTONUP:
            if not quit_confirm and not Popup.isActive():
                if len(orders) == 0 and not neworder:
                    neworder = True
                elif neworder and not settings and not pay and not paycompletedelay:
                    click_if()
                elif pay and not order.complete and not paycompletedelay and not settings:
                    click_pmenu()
                elif settings:
                    if settings_property == "setbuttonpos":
                        preset = "custom"
                        if cancelicon_sm.get_rect(center=(w/2+280, h/2-180)).collidepoint(pg.mouse.get_pos()):
                            settings = False
                        if buttonsoffsetxplus_rect.collidepoint(pg.mouse.get_pos()):
                            offset_btn_x += 1
                        if buttonsoffsetxminus_rect.collidepoint(pg.mouse.get_pos()):
                            offset_btn_x -= 1
                        if buttonsoffsetyplus_rect.collidepoint(pg.mouse.get_pos()):
                            offset_btn_y += 1
                        if buttonsoffsetyminus_rect.collidepoint(pg.mouse.get_pos()):
                            offset_btn_y -= 1
                        if textoffsetxplus_rect.collidepoint(pg.mouse.get_pos()):
                            offset_txt_x += 1
                        if textoffsetxminus_rect.collidepoint(pg.mouse.get_pos()):
                            offset_txt_x -= 1
                        if textoffsetyplus_rect.collidepoint(pg.mouse.get_pos()):
                            offset_txt_y += 1
                        if textoffsetyminus_rect.collidepoint(pg.mouse.get_pos()):
                            offset_txt_y -= 1
                        '''if buttonsoffsetxvaltext.get_rect(topleft=(w/2+200, h/2-30)).collidepoint(pg.mouse.get_pos()):
                            offset_btn_x = 0
                        if buttonsoffsetyvaltext.get_rect(topleft=(w/2+200, h/2)).collidepoint(pg.mouse.get_pos()):
                            offset_btn_y = 0
                        if textoffsetxvaltext.get_rect(topleft=(w/2+200, h/2+30)).collidepoint(pg.mouse.get_pos()):
                            offset_txt_x = 0
                        if textoffsetyvaltext.get_rect(topleft=(w/2+200, h/2+60)).collidepoint(pg.mouse.get_pos()):
                            offset_txt_y = 0'''
                        if spreadoffsetxplus_rect.collidepoint(pg.mouse.get_pos()):
                            spread_x += 0.01
                        if spreadoffsetxminus_rect.collidepoint(pg.mouse.get_pos()):
                            spread_x -= 0.01
                        if spreadoffsetyplus_rect.collidepoint(pg.mouse.get_pos()):
                            spread_y += 0.01
                        if spreadoffsetyminus_rect.collidepoint(pg.mouse.get_pos()):
                            spread_y -= 0.01
                        '''if spreadoffsetxvaltext.get_rect(topleft=(w/2+200, h/2+90)).collidepoint(pg.mouse.get_pos()):
                            spread_x = 0
                        if spreadoffsetyvaltext.get_rect(topleft=(w/2+200, h/2+120)).collidepoint(pg.mouse.get_pos()):
                            spread_y = 0'''
                        if sizemultiplierplus_rect.collidepoint(pg.mouse.get_pos()):
                            size_multiplier += 0.01
                        if sizemultiplierminus_rect.collidepoint(pg.mouse.get_pos()):
                            size_multiplier -= 0.01
                        if smallfonttextplus_rect.collidepoint(pg.mouse.get_pos()):
                            smallfont_size += 1
                            smallfont = pg.font.Font("assets/fonts/sysfont.ttf", smallfont_size)
                        if smallfonttextminus_rect.collidepoint(pg.mouse.get_pos()):
                            smallfont_size -= 1
                            smallfont = pg.font.Font("assets/fonts/sysfont.ttf", smallfont_size)
                        if fontsizetextplus_rect.collidepoint(pg.mouse.get_pos()):
                            font_size += 1
                            font = pg.font.Font("assets/fonts/sysfont.ttf", font_size)
                        if fontsizetextminus_rect.collidepoint(pg.mouse.get_pos()):
                            font_size -= 1
                            font = pg.font.Font("assets/fonts/sysfont.ttf", font_size)
                        if titlefontsizetextplus_rect.collidepoint(pg.mouse.get_pos()):
                            titlefont_size += 1
                            titlefont = pg.font.Font("assets/fonts/sysfont.ttf", titlefont_size)
                        if titlefontsizetextminus_rect.collidepoint(pg.mouse.get_pos()):
                            titlefont_size -= 1
                            titlefont = pg.font.Font("assets/fonts/sysfont.ttf", titlefont_size)
                        if neworderfontsizetextplus_rect.collidepoint(pg.mouse.get_pos()):
                            neworderfont_size += 1
                            neworderfont = pg.font.Font("assets/fonts/sysfont.ttf", neworderfont_size)
                        if neworderfontsizetextminus_rect.collidepoint(pg.mouse.get_pos()):
                            neworderfont_size -= 1
                            neworderfont = pg.font.Font("assets/fonts/sysfont.ttf", neworderfont_size)
                        if smallfontvaltext.get_rect(topleft=(w/2+200, h/2-180)).collidepoint(pg.mouse.get_pos()):
                            smallfont_size = 18
                            smallfont = pg.font.Font("assets/fonts/sysfont.ttf", smallfont_size)
                        if fontvaltext.get_rect(topleft=(w/2+200, h/2-150)).collidepoint(pg.mouse.get_pos()):
                            font_size = 30
                            font = pg.font.Font("assets/fonts/sysfont.ttf", font_size)
                        if titlefontvaltext.get_rect(topleft=(w/2+200, h/2-120)).collidepoint(pg.mouse.get_pos()):
                            titlefont_size = 60
                            titlefont = pg.font.Font("assets/fonts/sysfont.ttf", titlefont_size)
                        if neworderfontvaltext.get_rect(topleft=(w/2+200, h/2-90)).collidepoint(pg.mouse.get_pos()):
                            neworderfont_size = 25
                            neworderfont = pg.font.Font("assets/fonts/sysfont.ttf", neworderfont_size)
                    elif settings_property == "setdisplaysize":
                        if cancelicon_sm.get_rect(center=(w/2+120, h/2-180)).collidepoint(pg.mouse.get_pos()):
                            settings = False
                        row = 0
                        for k, v in enumerate(presets):
                            if pg.Rect(w/2-200, h/2-175+row*30, 400, 30).collidepoint(pg.mouse.get_pos()):
                                print(f"Selected: {k}, value: {v}")
                                size_multiplier = presets[v]["offsets"]["size_multiplier"]
                                keypad_mul = presets[v]["offsets"]["keypad_mul"]
                                button_sizing = presets[v]["offsets"]["button_sizing"]
                                offset_btn_x = presets[v]["offsets"]["offset_btn_x"]
                                offset_btn_y = presets[v]["offsets"]["offset_btn_y"]
                                offset_txt_x = presets[v]["offsets"]["offset_txt_x"]
                                offset_txt_y = presets[v]["offsets"]["offset_txt_y"]
                                spread_x = presets[v]["offsets"]["spread_x"]
                                spread_y = presets[v]["offsets"]["spread_y"]
                                smallfont_size = presets[v]["fontsize"]["smallfont"]
                                font_size = presets[v]["fontsize"]["font"]
                                titlefont_size = presets[v]["fontsize"]["titlefont"]
                                neworderfont_size = presets[v]["fontsize"]["neworderfont"]
                                preset = v
                            row += 1

                if switch_view == "bigger-buttons":
                    add = False
                    if pg.Rect(w/2-160, h/2-160, 90, 90).collidepoint(pg.mouse.get_pos()):
                        if num < 10:
                            num = num * 10 + 1
                        else:
                            addnum = 1
                            add = True
                    if pg.Rect(w/2-50, h/2-160, 90, 90).collidepoint(pg.mouse.get_pos()):
                        addnum = 2
                        add = True
                    if pg.Rect(w/2+60, h/2-160, 90, 90).collidepoint(pg.mouse.get_pos()):
                        addnum = 3
                        add = True
                    if pg.Rect(w/2-160, h/2-50, 90, 90).collidepoint(pg.mouse.get_pos()):
                        addnum = 4
                        add = True
                    if pg.Rect(w/2-50, h/2-50, 90, 90).collidepoint(pg.mouse.get_pos()):
                        addnum = 5
                        add = True
                    if pg.Rect(w/2+60, h/2-50, 90, 90).collidepoint(pg.mouse.get_pos()):
                        addnum = 6
                        add = True
                    if pg.Rect(w/2-160, h/2+60, 90, 90).collidepoint(pg.mouse.get_pos()):
                        addnum = 7
                        add = True
                    if pg.Rect(w/2-50, h/2+60, 90, 90).collidepoint(pg.mouse.get_pos()):
                        addnum = 8
                        add = True
                    if pg.Rect(w/2+60, h/2+60, 90, 90).collidepoint(pg.mouse.get_pos()):
                        addnum = 9
                        add = True
                    if pg.Rect(w/2-160, h/2+170, 90, 90).collidepoint(pg.mouse.get_pos()):
                        num = 1
                        addnum = 0
                    if pg.Rect(w/2-50, h/2+170, 90, 90).collidepoint(pg.mouse.get_pos()):
                        addnum = 0
                        if num == 1:
                            num = 10
                        else:
                            add = True

                    if pg.Rect(w/2+60, h/2+170, 90, 90).collidepoint(pg.mouse.get_pos()):
                        switch_view = "buttons"
                        item_count = num
                        num = 1
                        addnum = 1
                    elif add:
                        if num > 1:
                            num = num * 10 + addnum
                        else:
                            num = addnum
            elif quit_confirm:
                if quit_confirm_confirm.collidepoint(pg.mouse.get_pos()):
                    mainloop = False
                if quit_confirm_cancel.collidepoint(pg.mouse.get_pos()):
                    quit_confirm = False
            elif Popup.isActive():
                for popup in popups:
                    popups[popup].click()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                quit_confirm = True
            if event.key == pg.K_e:
                settings = not settings
    screen.fill((0, 0, 0))

    screen.blit(logo_small, logo_small.get_rect(topleft=(w/2-150, 2)))
    pg.draw.rect(screen, (255, 255, 255), (20, -20, 400, 70), border_radius=15)
    pg.draw.rect(screen, (255, 255, 255), (450, -20, 400, 70), border_radius=15)
    screen.blit(font.render(f"{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}", True, (0, 0, 0)), (90, 7))
    screen.blit(font.render(f"{username}", True, (0, 0, 0)), (510, 7))
    screen.blit(clockicon, clockicon.get_rect(center=(55, 20)))
    screen.blit(personicon, personicon.get_rect(center=(480, 18)))

    if len(orders) == 0 and not neworder and not paycompletedelay:
        pg.draw.rect(surface, (255, 255, 255), (50, 150, w-100, h-200), 3, border_radius=30)
        screen.blit(no_order_text, no_order_text.get_rect(center=(w/2, h/2-50)))
        screen.blit(no_order_subtitle, no_order_subtitle.get_rect(center=(w/2, h/2+50)))
    elif len(orders) != 0 and not neworder and not paycompletedelay:
        pg.draw.rect(surface, (255, 255, 255), (50, 150, w-100, h-200), 3, border_radius=30)
        screen.blit(font.render("van rendelés lol", True, (255, 255, 255)), (w/2, h/2))
    elif neworder or paycompletedelay:
        pg.draw.rect(surface, (255, 255, 255), (w/4+10, 150, w-w/4-50, h-200), 3, border_radius=15)
        pg.draw.rect(surface, (255, 255, 255), (30, 150, w/4-50, h-200), 3, border_radius=15)
        try:
            if pay or paycompletedelay:
                draw_pmenu()
            else:
                draw_if()
                draw_neworder()
        except Exception as e:
            error("general", 10, "main.py", e)

        for popup in popups:
            popups[popup].draw()
    
    if switch_view == "bigger-buttons":
        #draw numpad rects
        pg.draw.rect(surface, (255, 255, 255), (w/2-180, h/2-300, 350, 600), border_radius=30)

        pg.draw.rect(surface, (200, 200, 200), (w/2-160, h/2-280, 310, 100), border_radius=30)

        pg.draw.rect(surface, (200, 200, 200), (w/2-160, h/2-160, 90, 90), border_radius=30)
        pg.draw.rect(surface, (200, 200, 200), (w/2-50, h/2-160, 90, 90), border_radius=30)
        pg.draw.rect(surface, (200, 200, 200), (w/2+60, h/2-160, 90, 90), border_radius=30)

        row1 = titlefont_bold.render("1    2    3", True, (0, 0, 0))
        screen.blit(row1, row1.get_rect(center=(w/2, h/2-120)))

        pg.draw.rect(surface, (200, 200, 200), (w/2-160, h/2-50, 90, 90), border_radius=30)
        pg.draw.rect(surface, (200, 200, 200), (w/2-50, h/2-50, 90, 90), border_radius=30)
        pg.draw.rect(surface, (200, 200, 200), (w/2+60, h/2-50, 90, 90), border_radius=30)

        row2 = titlefont_bold.render("4    5    6", True, (0, 0, 0))
        screen.blit(row2, row2.get_rect(center=(w/2, h/2-10)))

        pg.draw.rect(surface, (200, 200, 200), (w/2-160, h/2+60, 90, 90), border_radius=30)
        pg.draw.rect(surface, (200, 200, 200), (w/2-50, h/2+60, 90, 90), border_radius=30)
        pg.draw.rect(surface, (200, 200, 200), (w/2+60, h/2+60, 90, 90), border_radius=30)

        row3 = titlefont_bold.render("7    8    9", True, (0, 0, 0))
        screen.blit(row3, row3.get_rect(center=(w/2, h/2+100)))
        
        pg.draw.rect(surface, (200, 200, 200), (w/2-160, h/2+170, 90, 90), border_radius=30)
        pg.draw.rect(surface, (200, 200, 200), (w/2-50, h/2+170, 90, 90), border_radius=30)
        pg.draw.rect(surface, (200, 200, 200), (w/2+60, h/2+170, 90, 90), border_radius=30)

        row4 = titlefont_bold.render("C    0    #", True, (0, 0, 0))
        screen.blit(row4, row4.get_rect(center=(w/2, h/2+210)))

        screen.blit(titlefont.render(str(num), True, (0, 0, 0)), titlefont.render(str(num), True, (0, 0, 0)).get_rect(center=(w/2, h/2-250)))

    if settings:
        if settings_property == "setbuttonpos":
            pg.draw.rect(screen, (0, 0, 0), (w/2-301, h/2-201, 602, 372))
            pg.draw.rect(screen, (225, 225, 225), (w/2-300, h/2-200, 600, 370))
            settitle = font.render("Settings", True, (0, 0, 0))
            smallfonttext = font.render("Small font size", True, (0, 0, 0))
            screen.blit(smallfonttext, smallfonttext.get_rect(topleft=(w/2-290, h/2-180)))
            fontsizetext = font.render("Normal font size", True, (0, 0, 0))
            screen.blit(fontsizetext, fontsizetext.get_rect(topleft=(w/2-290, h/2-150)))
            titlefonttext = font.render("Titles font size", True, (0, 0, 0))
            screen.blit(titlefonttext, titlefonttext.get_rect(topleft=(w/2-290, h/2-120)))
            neworderfonttext = font.render("Items font size", True, (0, 0, 0))
            screen.blit(neworderfonttext, neworderfonttext.get_rect(topleft=(w/2-290, h/2-90)))
            screen.blit(settitle, settitle.get_rect(center=(w/2, h/2-180)))
            sizemultipliertext = font.render("Size multiplier", True, (0, 0, 0))
            screen.blit(sizemultipliertext, sizemultipliertext.get_rect(topleft=(w/2-290, h/2-60)))
            buttonsoffsetxtext = font.render("buttons ofsset X", True, (0, 0, 0))
            screen.blit(buttonsoffsetxtext, buttonsoffsetxtext.get_rect(topleft=(w/2-290, h/2-30)))
            buttonsoffsetytext = font.render("buttons ofsset Y", True, (0, 0, 0))
            screen.blit(buttonsoffsetytext, buttonsoffsetytext.get_rect(topleft=(w/2-290, h/2)))
            textoffsetxtext = font.render("Text ofsset X", True, (0, 0, 0))
            screen.blit(textoffsetxtext, textoffsetxtext.get_rect(topleft=(w/2-290, h/2+30)))
            textoffsetytext = font.render("Text ofsset Y", True, (0, 0, 0))
            screen.blit(textoffsetytext, textoffsetytext.get_rect(topleft=(w/2-290, h/2+60)))
            spreadoffsetxtext = font.render("Spread offset X", True, (0, 0, 0))
            screen.blit(spreadoffsetxtext, spreadoffsetxtext.get_rect(topleft=(w/2-290, h/2+90)))
            spreadoffsetytext = font.render("Spread offset Y", True, (0, 0, 0))
            screen.blit(spreadoffsetytext, spreadoffsetytext.get_rect(topleft=(w/2-290, h/2+120)))
            sizemultipliervaltext = font.render(str(round(size_multiplier, 2)), True, (0, 0, 0))
            buttonsoffsetxvaltext = font.render(str(offset_btn_x), True, (0, 0, 0))
            buttonsoffsetyvaltext = font.render(str(offset_btn_y), True, (0, 0, 0))
            textoffsetxvaltext = font.render(str(offset_txt_x), True, (0, 0, 0))
            textoffsetyvaltext = font.render(str(offset_txt_y), True, (0, 0, 0))
            fontsizetextval = font.render(str(font_size), True, (0, 0, 0))
            titlefontsizetextval = font.render(str(titlefont_size), True, (0, 0, 0))
            neworderfontsizetextval = font.render(str(neworderfont_size), True, (0, 0, 0))
            smallfonttextval = font.render(str(smallfont_size), True, (0, 0, 0))
            screen.blit(plus, sizemultiplierplus_rect)
            screen.blit(minus, sizemultiplierminus_rect)
            screen.blit(plus, smallfonttextplus_rect)
            screen.blit(minus, smallfonttextminus_rect)
            screen.blit(plus, fontsizetextplus_rect)
            screen.blit(minus, fontsizetextminus_rect)
            screen.blit(plus, titlefontsizetextplus_rect)
            screen.blit(minus, titlefontsizetextminus_rect)
            screen.blit(plus, neworderfontsizetextplus_rect)
            screen.blit(minus, neworderfontsizetextminus_rect)
            screen.blit(smallfonttextval, smallfonttextval.get_rect(topleft=(w/2+200, h/2-180)))
            screen.blit(fontsizetextval, fontsizetextval.get_rect(topleft=(w/2+200, h/2-150)))
            screen.blit(titlefontsizetextval, titlefontsizetextval.get_rect(topleft=(w/2+200, h/2-120)))
            screen.blit(neworderfontsizetextval, neworderfontsizetextval.get_rect(topleft=(w/2+200, h/2-90)))
            screen.blit(sizemultipliervaltext, sizemultipliervaltext.get_rect(center=(w/2+200, h/2-45)))
            screen.blit(buttonsoffsetxtext, buttonsoffsetxtext.get_rect(topleft=(w/2-290, h/2-30)))
            screen.blit(buttonsoffsetxvaltext, buttonsoffsetxvaltext.get_rect(center=(w/2+200, h/2-15)))
            screen.blit(buttonsoffsetyvaltext, buttonsoffsetyvaltext.get_rect(center=(w/2+200, h/2+15)))
            screen.blit(textoffsetxvaltext, textoffsetxvaltext.get_rect(center=(w/2+200, h/2+45)))
            screen.blit(textoffsetyvaltext, textoffsetyvaltext.get_rect(center=(w/2+200, h/2+75)))
            screen.blit(plus, buttonsoffsetxplus_rect)
            screen.blit(minus, buttonsoffsetxminus_rect)
            screen.blit(plus, buttonsoffsetyplus_rect)
            screen.blit(minus, buttonsoffsetyminus_rect)
            screen.blit(plus, textoffsetxplus_rect)
            screen.blit(minus, textoffsetxminus_rect)
            screen.blit(plus, textoffsetyplus_rect)
            screen.blit(minus, textoffsetyminus_rect)
            screen.blit(plus, spreadoffsetxplus_rect)
            screen.blit(minus, spreadoffsetxminus_rect)
            screen.blit(plus, spreadoffsetyplus_rect)
            screen.blit(minus, spreadoffsetyminus_rect)
            spreadoffsetxvaltext = font.render(str(round(spread_x, 2)), True, (0, 0, 0))
            spreadoffsetyvaltext = font.render(str(round(spread_y, 2)), True, (0, 0, 0))
            screen.blit(spreadoffsetxvaltext, spreadoffsetxvaltext.get_rect(center=(w/2+200, h/2+110)))
            screen.blit(spreadoffsetyvaltext, spreadoffsetyvaltext.get_rect(center=(w/2+200, h/2+140)))
            screen.blit(cancelicon_sm, cancelicon_sm.get_rect(center=(w/2+280, h/2-180)))
        elif settings_property == "setdisplaysize":
            pg.draw.rect(screen, (0, 0, 0), (w/2-151, h/2-201, 302, 372))
            pg.draw.rect(screen, (225, 225, 225), (w/2-150, h/2-200, 300, 370))
            row = 0
            for k, v in enumerate(presets):
                if pg.Rect(w/2-200, h/2-175+row*30, 400, 30).collidepoint(pg.mouse.get_pos()):
                    pg.draw.rect(screen, (200, 200, 200), (w/2-150, h/2-175+row*30, 300, 30))
                size = font.render(f"{v.replace('x', ' x ')}", True, (0, 0, 0))
                screen.blit(size, size.get_rect(center=(w/2, h/2-165 + (row*30))))
                row += 1
            screen.blit(cancelicon_sm, cancelicon_sm.get_rect(center=(w/2+130, h/2-180)))
            screeninfo = smallfont.render(f"Kijelző: {w} x {h}", True, (0, 0, 0))
            screen.blit(screeninfo, screeninfo.get_rect(center=(w/2, h/2+100)))
            currentinfo = smallfont.render(f"Jelenleg: {preset}", True, (0, 0, 0))
            screen.blit(currentinfo, currentinfo.get_rect(center=(w/2, h/2+120)))

    if quit_confirm:
        pg.draw.rect(screen, (0, 0, 0), (w/2-501, h/2-101, 1002, 202), border_radius=40)
        pg.draw.rect(screen, (225, 225, 225), (w/2-500, h/2-100, 1000, 200), border_radius=40)
        screen.blit(titlefont.render("Biztosan kilép?", True, (0, 0, 0)), (w/2-250, h/2-80))
        screen.blit(font.render("A nem mentett adatok elvesznek.", True, (0, 0, 00)), (w/2-240, h/2-10))
        pg.draw.rect(screen, (255, 0, 0), quit_confirm_confirm, border_radius=20)
        pg.draw.rect(screen, (200, 200, 200), quit_confirm_cancel, border_radius=20)
        screen.blit(font.render("Kilépés", True, (255, 255, 255)), (quit_confirm_confirm.topleft[0]+45, quit_confirm_confirm.topleft[1]+5))
        screen.blit(font.render("Mégse", True, (0, 0, 0)), (quit_confirm_cancel.topleft[0]+45, quit_confirm_cancel.topleft[1]+5))
        screen.blit(warnicon, warnicon.get_rect(center=(w/2-380, h/2)))
    pg.display.flip()

screen.fill((0, 0, 0))
screen.blit(logo, logo.get_rect(center=(w/2, h/2-200)))
screen.blit(titlefont.render("Mentés és kilépés...", True, (255, 255, 255)), titlefont.render("Mentés és kilépés...", True, (255, 255, 255)).get_rect(center=(w/2, h/2+100)))
pg.display.flip()
time.sleep(2)
pg.quit()


with open("interface/settings.json", "w", encoding="utf-8") as save:
    write = {
            "offsets": {
                "offset_btn_x": offset_btn_x,
                "offset_txt_x": offset_txt_x,
                "offset_btn_y": offset_btn_y,
                "offset_txt_y": offset_txt_y,
                "spread_x": spread_x,
                "spread_y": spread_y,
                "size_multiplier": size_multiplier,
                "keypad_mul": [keypad_mul[0], keypad_mul[1], keypad_mul[2], keypad_mul[3], keypad_mul[4]],
                "button_sizing": [button_sizing[0], button_sizing[1], button_sizing[2]]
            },
            "fontsize":{
                "smallfont": smallfont_size,
                "font": font_size,
                "titlefont": titlefont_size,
                "neworderfont": neworderfont_size
            },
            "preset": preset
    }
    dump(write, save, indent=4)
    print("saved settings")

with open("orders.json", "w", encoding="utf-8") as save:
    for order in orders_complete:
        add_data = {
            "num": order.num,
            "items":order.items,
            "price":order.get_price(),
            "time":order.time,
            "paymentmethod":order.paymentmethod,
            "paid":order.paid,
        }
        orders_loaded["orders"].append(add_data)
    dump(orders_loaded, save, indent=4)
    print("saved orders")