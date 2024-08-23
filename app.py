import pygame
import sys
import pyttsx3

# Khởi tạo Pygame
pygame.init()

# Màu sắc
WHITE = (255, 255, 255)
SILVER = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)


# Cấu hình cửa sổ
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TỪ ĐIỂN ENGLISH - ENGLISH")

# Load images
board_img = pygame.image.load('board.jpg')
board_img = pygame.transform.scale(board_img, (WIDTH, HEIGHT))

#Cấu hình xuống dòng (chung)
max_width_line = 550

#Cấu hình màu
color_fill = SILVER
color_write = BLACK
color_border = BLACK
color_border2 = WHITE
color_label = BLUE
color_button = YELLOW
color_button2 = GREEN
color_button3 = RED

# Font
font = pygame.font.Font(None, 32)

#Công cụ đọc từ tiếng anh
def speak_word(word):
    engine = pyttsx3.init()
    engine.setProperty('rate', 100)
    engine.say(word)
    engine.runAndWait()
##############################################################
class WordEntry:
    def __init__(self, word, word_type, definition, example):
        self.word = word
        self.word_type = word_type
        self.definition = definition
        self.example = example
        self.next = None

    def validate(self):
        # Kiểm tra từng thuộc tính
        if self.word.isalpha() and self.word_type.isalpha() and any(char.isalnum() for char in self.definition) and any(char.isalnum() for char in self.example):
            return True
        else:
            return False

class HashTable:
    def __init__(self, size=26):
        self.size = size
        self.entries = [None] * size

    def hash_function(self, word):
        if word == '':
            return -1
        else:
            if word[0].lower().isalpha():
                return ord(word[0].lower()) - ord('a')
            else:
                return -1

    def insert(self, word_entry):
        index = self.hash_function(word_entry.word)
        if self.entries[index] is None:
            self.entries[index] = word_entry
        else:
            if self.search(word_entry.word) is None:
                current = self.entries[index]
                while current.next:
                    current = current.next
                current.next = word_entry

    def search(self, word):
        index = self.hash_function(word)
        if index != -1 :
            current = self.entries[index]
            while current:
                if current.word == word:
                    return current
                current = current.next
        else:
            return None

    def delete(self, word):
        index = self.hash_function(word)
        if index != -1:
            current = self.entries[index]
            prev = None
            while current:
                if current.word == word:
                    if prev:
                        prev.next = current.next
                    else:
                        self.entries[index] = current.next
                    return
                prev = current
                current = current.next

class Dictionary:
    def __init__(self):
        self.hash_table = HashTable()

    def load_from_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                word = parts[0].strip()
                word_type = parts[1].strip()
                definition = parts[2].strip()
                example = parts[3].strip()
                word_entry = WordEntry(word, word_type, definition, example)
                self.hash_table.insert(word_entry)

    def search_word(self, word):
        return self.hash_table.search(word)

    def add_word(self, word_entry):
        existing_entry = self.search_word(word_entry.word)
        if existing_entry:
            existing_entry.word_type = word_entry.word_type
            existing_entry.definition = word_entry.definition
            existing_entry.example = word_entry.example
        else:
            self.hash_table.insert(word_entry)

    def delete_word(self, word):
        return self.hash_table.delete(word)

    def reload_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            for entry_list in self.hash_table.entries:
                current = entry_list
                while current:
                    file.write(f"{current.word}|{current.word_type}|{current.definition}|{current.example}\n")
                    current = current.next

###############################################################################################################
def draw_text_1Line(surface, text, x, y, color):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def draw_text(surface, text, x, y, color, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    
    for word in words:
        test_line = current_line + word + ' '
        test_width, _ = font.size(test_line)
        
        if test_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ' '
    
    # Thêm dòng cuối cùng
    lines.append(current_line)
    
    # Vẽ từng dòng
    for line in lines:
        draw_text_1Line(surface, line, x, y, color)
        y += font.get_height()  # Dịch xuống dòng tiếp theo


def Display_text(result_frame, word_entry, word_box, word_type_box, definition_box, example_box, number_active_box):
    #Vẽ viền khung
    pygame.draw.rect(window, color_border, word_box, 2)
    pygame.draw.rect(window, color_border, word_type_box, 2)
    pygame.draw.rect(window, color_border, definition_box, 2)
    pygame.draw.rect(window, color_border, example_box, 2)

    #Tạo hiệu ứng focus đơn giản
    if number_active_box == 1:
        pygame.draw.rect(window, color_border2, word_box, 2)
    elif number_active_box == 2:
        pygame.draw.rect(window, color_border2, word_type_box, 2)
    elif number_active_box == 3:
        pygame.draw.rect(window, color_border2, definition_box, 2)
    elif number_active_box == 4:
        pygame.draw.rect(window, color_border2, example_box, 2)

    #vẽ label
    draw_text_1Line(window, "WORD", word_box.x - 130, word_box.y + 15, color_label)
    draw_text_1Line(window, "TYPE", word_type_box.x - 130, word_type_box.y, color_label)
    draw_text_1Line(window, "MEANING", definition_box.x - 130, definition_box.y + 50, color_label)
    draw_text_1Line(window, "EXAMPLE", example_box.x - 130, example_box.y + 50, color_label)

    #Kiểm tra và hiển thị
    if word_entry is not None:
        draw_text(window, word_entry.word, word_box.x + 10, word_box.y + 10, color_write, max_width_line)
        draw_text(window, word_entry.word_type, word_type_box.x + 10, word_type_box.y + 5, color_write, max_width_line)
        draw_text(window, word_entry.definition, definition_box.x + 10, definition_box.y + 10, color_write, max_width_line)
        draw_text(window, word_entry.example, example_box.x + 10, example_box.y + 10, color_write, max_width_line)

def CheckPopup():
    popup_box = pygame.Rect(250, 200, 300, 200)
    yes_button = pygame.Rect(popup_box.left+33, popup_box.top+120, 100, 50)
    no_button = pygame.Rect(popup_box.left+166, popup_box.top+120, 100, 50)
    while True:
        pygame.draw.rect(window, color_fill, popup_box)
        pygame.draw.rect(window, color_button3, yes_button)
        pygame.draw.rect(window, color_button2, no_button)
        draw_text_1Line(window, "ARE YOU SURE?", popup_box.x + 60, popup_box.y + 70, color_write)
        draw_text_1Line(window, "YES", yes_button.x + 25, yes_button.y + 20, color_write)
        draw_text_1Line(window, "NO", no_button.x + 30, no_button.y + 20, color_write)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):  
                    return True
                elif no_button.collidepoint(event.pos):  
                    return False

        pygame.display.flip()

def main():
    #Khung Search
    Search_box = pygame.Rect(60, 70, 250, 40)
    # Nút MODE, nút ADD, nút DEL
    MODE_button = pygame.Rect(320, 30, 160, 80)
    ADD_button = pygame.Rect(530, 30, 100, 80)
    DEL_button = pygame.Rect(640, 30, 100, 80)
    # Khung hiển thị kết quả tra cứu
    result_frame = pygame.Rect(180, 120, max_width_line+20, 400)
    # Các khung thông tin
    word_box = pygame.Rect(result_frame.left + 10, result_frame.top + 10, result_frame.width - 20, 50)
    word_type_box = pygame.Rect(result_frame.left + 10, word_box.bottom + 10, result_frame.width - 20, 30)
    definition_box = pygame.Rect(result_frame.left + 10, word_type_box.bottom + 10, result_frame.width - 20, 150)
    example_box = pygame.Rect(result_frame.left + 10, definition_box.bottom + 10, result_frame.width - 20, 150)
    #Nút đọc to từ tiếng anh
    SPEAK_button = pygame.Rect(30, 530, 100, 50)

    # Khởi tạo biến từ điển và nạp dữ liệu từ điển
    dictionary = Dictionary()
    dictionary.load_from_file('data.txt')

    #Các biến sử dụng trong chế độ tra cứu
    active = False
    search_text = ''

    #Các biến sử dụng trong chế độ thêm/bớt
    active_MODE = False
    number_active_box = 0
    text = ' '

    #Biến đặc biệt
    word_entry = WordEntry("", "", "", "")
    running = True

    #Thiết lập Clock
    clock = pygame.time.Clock()

    while running:
        window.fill(WHITE)

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #Sự kiện nhấn nút thoát
                running = False     #Hiển nhiên là THOÁT =)))))
            elif event.type == pygame.MOUSEBUTTONDOWN:  #Sự kiện click chuột
                text = ''   #Biến này lưu trữ tạm thời cho chế độ MODE nên sẽ được reset khi có sự kiện click chuột
                if SPEAK_button.collidepoint(event.pos):   #Click vào nút đọc từ tiếng anh
                    if word_entry.validate() and active_MODE is False:
                        speak_word(word_entry.word)     #Đọc to từ tiếng anh

                elif Search_box.collidepoint(event.pos):   #Click vào khung Search
                    active = not active     #Đảo trạng thái của biến này để bật/tắt chế độ tra cứu
                    active_MODE = False     #Tắt chế độ thêm/bớt từ
                    word_entry = WordEntry("", "", "", "")  #Biến này sẽ được reset mỗi khi vào thay đổi chế độ
                    number_active_box = 0   #Biến này được reset để tránh focus vào khung thông tin nào đó

                elif MODE_button.collidepoint(event.pos):     #Click vào nút MODE
                    active_MODE = not active_MODE       #Đảo trạng thái của biến này để bật/tắt chế độ thêm/bớt từ
                    active = False      #Tắt chế độ tra cứu
                    word_entry = WordEntry("", "", "", "")      #Biến này sẽ được reset mỗi khi vào thay đổi chế độ
                    number_active_box = 0       #Biến này được reset để tránh focus vào khung thông tin nào đó

                elif active_MODE:     #Các sự kiện click chuột vào khung thông tin chỉ được ghi nhận khi ở chế độ thêm/bớt từ, number_box sẽ được chọn tương ứng
                    if word_box.collidepoint(event.pos):
                        number_active_box = 1
                        text = word_entry.word
                    elif word_type_box.collidepoint(event.pos):
                        number_active_box = 2
                        text = word_entry.word_type
                    elif definition_box.collidepoint(event.pos):
                        number_active_box = 3
                        text = word_entry.definition
                    elif example_box.collidepoint(event.pos):
                        number_active_box = 4
                        text = word_entry.example # Biến text lấy dữ liệu như vậy để tiện việc chỉnh sửa các khung thông tin
                    elif ADD_button.collidepoint(event.pos):  #Click chuột vào nút ADD
                        if word_entry.validate():   #Kiểm tra các khung thông tin đã điền hết chưa bằng phương thức validate()
                            isYes = CheckPopup()    #Tạo check pop up để xác nhận việc nhấn nút
                            if isYes:
                                number_active_box = 0   #Biến này được reset để tránh focus vào khung thông tin nào đó
                                dictionary.add_word(word_entry)     #Sử dụng phương thức thêm từ vào từ điển
                                dictionary.reload_to_file('data.txt')   #Nạp lại vào từ điển
                                active_MODE = False     #Tắt chế độ thêm/bớt từ
                                word_entry = WordEntry("", "", "", "")  #Biến này sẽ được reset mỗi khi vào thay đổi chế độ
                    elif DEL_button.collidepoint(event.pos):  #Click chuột vào nút DEL
                        if word_entry.validate():   #Kiểm tra các khung thông tin đã điền hết chưa bằng phương thức validate()
                            isYes = CheckPopup()    #Tạo check pop up để xác nhận việc nhấn nút
                            if isYes:
                                number_active_box = 0   #Biến này được reset để tránh focus vào khung thông tin nào đó
                                dictionary.delete_word(word_entry.word)     #Sử dụng phương thức thêm từ vào từ điển
                                dictionary.reload_to_file('data.txt')   #Nạp lại vào từ điển
                                active_MODE = False     #Tắt chế độ thêm/bớt từ
                                word_entry = WordEntry("", "", "", "")  #Biến này sẽ được reset mỗi khi vào thay đổi chế độ

            elif event.type == pygame.KEYDOWN:  #Sự kiện gõ phím
                if active:  # Chế độ tra cứu
                    if event.key == pygame.K_RETURN:    #Ghi nhận kí tự ENTER
                        if dictionary.search_word(search_text.lower()) is not None:
                            word_entry = dictionary.search_word(search_text.lower())
                            search_text = ''    #Biến này reset để khung search trống sau khi tra cứu thành công
                            active = False      #Tắt chế độ tra cứu

                    elif event.key == pygame.K_BACKSPACE:   #Ghi nhận kí tự BACKSPACE
                        search_text = search_text[:-1]      #Xóa bớt kí tự cuối
                    elif event.unicode.isalpha():   #Ghi nhận kí tự là chữ cái
                        search_text += event.unicode

                elif active_MODE:     # Chế độ thêm/bớt từ
                    if event.key == pygame.K_RETURN:    #Ghi nhận kí tự ENTER
                        text = text     #Nothing =)))) Chủ yếu để chống lỗi
                    elif event.key == pygame.K_BACKSPACE:     #Ghi nhận kí tự BACKSPACE
                        text = text[:-1]    #Xóa bớt kí tự cuối
                    elif event.unicode.isalpha() or number_active_box > 2:#Ghi nhận kí tự là chữ cái (lưu ý khung 3 và 4 có thể chứa kí tự không phải là chữ cái)
                        text += event.unicode

                    #Điều khiển dữ liệu nhập vào đúng vị trí bằng number_box
                    if number_active_box == 1:
                        text = text.lower()
                         #Hỗ trợ phát hiện từ vựng đã có trong từ điển
                        if dictionary.search_word(text) is not None:
                            new_word_entry = dictionary.search_word(text)
                            word_entry.word = new_word_entry.word
                            word_entry.word_type = new_word_entry.word_type
                            word_entry.definition = new_word_entry.definition
                            word_entry.example = new_word_entry.example
                        else:
                            word_entry.word = text
                            
                    elif number_active_box == 2:
                        word_entry.word_type = text
                    elif number_active_box == 3:
                        word_entry.definition = text
                    elif number_active_box == 4:
                        word_entry.example = text

        #Sử dụng quét màn hình để hiển thị
        #Tạo nền
        window.blit(board_img, (0, 0))

        # Vẽ ô nhập
        draw_text_1Line(window, "Search:", Search_box.x, Search_box.y - 25, color_label)
        if active:  #Chế độ màu và viền khung search khi ở chế độ tra cứu
            pygame.draw.rect(window, color_border, Search_box, 2)    #Vẽ viền khung
            draw_text_1Line(window, search_text, Search_box.x + 5, Search_box.y + 10, color_write)
        else:   #Chế độ màu và viền khung search khi KHÔNG ở chế độ tra cứu (có thêm text<> để nhận biết)
            pygame.draw.rect(window, color_fill, Search_box)     #Vẽ viền khung
            draw_text_1Line(window, "<Click here>", Search_box.x + 50, Search_box.y + 10, color_write)
        
        # Vẽ nút MODE và ADD, DEL
        if active_MODE:     #Hiển thị nút ADD, DEL và focus vào nút MODE khi ở chế độ thêm/bớt từ
            pygame.draw.rect(window, color_button, MODE_button)     #Vẽ viền khung
            if word_entry.validate():
                pygame.draw.rect(window, color_button2, ADD_button)       #Vẽ viền khung
                pygame.draw.rect(window, color_button3, DEL_button)       #Vẽ viền khung
            else:
                pygame.draw.rect(window, color_button2, ADD_button, 2)       #Vẽ viền khung
                pygame.draw.rect(window, color_button3, DEL_button, 2)       #Vẽ viền khung
            draw_text_1Line(window, "ADD", ADD_button.x + 25, ADD_button.y + 25, color_write)
            draw_text_1Line(window, "DEL", DEL_button.x + 25, DEL_button.y + 25, color_write)
        else:   #Chỉ in nút MODE và bỏ focus vào nút MODE khi KHÔNG ở chế độ thêm/bớt từ
            pygame.draw.rect(window, color_button, MODE_button, 2)      #Vẽ viền khung
        draw_text_1Line(window, "MODE", MODE_button.x + 45, MODE_button.y + 25, color_write)

        #Vẽ nút đọc từ tiếng anh
        if word_entry.validate() and active_MODE is False:    #Xử lí viền theo khung thông tin và trạng thái chế độ thêm/bớt từ
            pygame.draw.rect(window, color_button2, SPEAK_button)
        else:
            pygame.draw.rect(window, color_button2, SPEAK_button, 2)    
        draw_text_1Line(window, "SPEAK", SPEAK_button.x + 10, SPEAK_button.y + 15, color_write)
        
        #Vẽ khung thông tin
        Display_text(result_frame, word_entry, word_box, word_type_box, definition_box, example_box, number_active_box)

        pygame.display.update()  # Cập nhật màn hình
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
