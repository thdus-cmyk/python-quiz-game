import json
import os

class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question  # 문제 내용
        self.choices = choices    # 선택지 4개 (리스트 형태)
        self.answer = answer      # 정답 번호 (1~4)

    def display(self):
        """퀴즈를 화면에 출력하는 메서드"""
        print(f"\n[문제]")
        print(self.question)
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")

    def check_answer(self, user_answer):
        """사용자가 입력한 답이 정답인지 확인하는 메서드"""
        return user_answer == self.answer
        # --- 기본 퀴즈 데이터 생성 ---
# 본인이 선택한 주제의 퀴즈 5개 이상을 Quiz 클래스의 인스턴스로 만듭니다.
quiz_1 = Quiz(
    "다음 중 가장 성격이 나쁜 강아지는?",
    ["골든 리트리버", "시츄", "치와와", "사모예드"],
    3
)

quiz_2 = Quiz(
    "성심당에서 팔지 않는 것은?",
    ["명란 바게트", "튀김 소보로", "딸기시루", "한방능이백숙"],
    4
)

quiz_3 = Quiz(
    "빛의 삼원색이 아닌 것은?",
    ["노랑", "빨강", "파랑", "초록"],
    1
)

quiz_4 = Quiz(
    "대전 출신이 아닌 연예인은?",
    ["설윤", "안유진", "카리나", "조보아"],
    3
)

quiz_5 = Quiz(
    "「낮말은 새가 듣고 밤말은 O가 듣는다」여기서 O는?",
    ["공룡", "문어", "쥐", "개"],
    3
)

# 생성한 퀴즈들을 리스트에 담아둡니다.
initial_quizzes = [quiz_1, quiz_2, quiz_3, quiz_4, quiz_5]

# --- 파일 저장 및 불러오기 파일 경로 설정 ---
STATE_FILE = "state.json"

def load_game_data():
    """state.json 파일에서 퀴즈 목록과 최고 점수를 불러오는 함수"""
    # 파일이 아예 없거나 손상된 경우 기본 퀴즈 데이터와 초기 점수(0점) 반환
    if not os.path.exists(STATE_FILE):
        print("📁 저장된 데이터 파일이 없어 기본 퀴즈를 사용합니다.")
        return initial_quizzes, 0

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            # JSON 데이터를 Quiz 객체 리스트로 변환
            loaded_quizzes = []
            for q_data in data.get("quizzes", []):
                quiz = Quiz(q_data["question"], q_data["choices"], q_data["answer"])
                loaded_quizzes.append(quiz)
                
            best_score = data.get("best_score", 0)
            
            if not loaded_quizzes: # 리스트가 비어있다면 기본 퀴즈 사용
                return initial_quizzes, best_score
                
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(loaded_quizzes)}개, 최고점수 {best_score}점)")
            return loaded_quizzes, best_score

    except Exception as e:
        # 파일이 손상되었거나 읽기 오류가 발생한 경우 예외 처리
        print("⚠️ 파일이 손상되었거나 읽는 중 오류가 발생했습니다. 기본 데이터로 복구합니다.")
        return initial_quizzes, 0

def save_game_data(quizzes, best_score):
    """현재 퀴즈 목록과 최고 점수를 state.json 파일에 저장하는 함수"""
    # Quiz 객체 리스트를 JSON으로 저장할 수 있는 딕셔너리 형태로 변환
    quiz_list_data = []
    for q in quizzes:
        quiz_list_data.append({
            "question": q.question,
            "choices": q.choices,
            "answer": q.answer
        })
        
    data = {
        "quizzes": quiz_list_data,
        "best_score": best_score
    }
    
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"⚠️ 파일 저장 중 오류가 발생했습니다: {e}")
class QuizGame:
    def __init__(self):
        # 파일에서 퀴즈 목록과 최고 점수 불러오기
        self.quizzes, self.best_score = load_game_data()

    def display_menu(self):
        """메뉴 화면을 출력하는 메서드"""
        print("\n" + "=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯        ")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def run(self):
        """프로그램 실행 및 메뉴 선택을 관리하는 메인 메서드"""
        # 프로그램 실행 중 Ctrl+C(KeyboardInterrupt)나 EOFError 발생 시 안전하게 종료 처리
        try:
            while True:
                self.display_menu()
                
                # 사용자 입력 (앞뒤 공백 제거)[cite: 7]
                choice_str = input("선택: ").strip()
                
                # 빈 입력 처리 (그냥 Enter를 친 경우)[cite: 7]
                if not choice_str:
                    print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
                    continue
                    
                # 숫자 변환 실패 처리 (abc 등을 입력한 경우)[cite: 7]
                try:
                    choice = int(choice_str)
                except ValueError:
                    print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
                    continue
                    
                # 허용 범위 밖 숫자 처리 (1~5 외의 번호 입력 시)[cite: 7]
                if choice < 1 or choice > 5:
                    print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
                    continue
                    
                # 메뉴 기능 분기
                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.view_quizzes()
                elif choice == 4:
                    self.check_score()
                elif choice == 5:
                    print("\n👋 프로그램을 종료합니다. 이용해주셔서 감사합니다!")
                    break
                    
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 프로그램이 강제 중단되었습니다. 안전하게 저장 후 종료합니다.")
            save_game_data(self.quizzes, self.best_score)

    def play_quiz(self):
        """퀴즈 풀기 기능[cite: 1]"""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해주세요!")
            return
            
        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        correct_count = 0
        total = len(self.quizzes)
        
        for idx, quiz in enumerate(self.quizzes, 1):
            print("\n" + "-" * 40)
            print(f"[문제 {idx}]")
            print(quiz.question)
            for i, choice in enumerate(quiz.choices, 1):
                print(f"{i}. {choice}")
                
            while True:
                ans_str = input("\n정답 입력: ").strip()
                if not ans_str:
                    print("⚠️ 빈 입력입니다. 숫자를 입력해주세요.")
                    continue
                try:
                    ans = int(ans_str)
                    if ans < 1 or ans > 4:
                        print("⚠️ 1~4 사이의 숫자를 입력해주세요.")
                        continue
                    break
                except ValueError:
                    print("⚠️ 숫자 형식으로 입력해주세요.")
                    
            if quiz.check_answer(ans):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print(f"❌ 틀렸습니다! 정답은 {quiz.answer}번입니다.")
                
        # 점수 계산 (맞춘 개수 / 전체 개수 * 100)
        score = int((correct_count / total) * 100)
        
        print("\n" + "=" * 40)
        print(f"🏆 결과: 총 {total}문제 중 {correct_count}문제 정답! ({score}점)")
        
        # 최고 점수 비교 및 갱신[cite: 2]
        if score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")
            save_game_data(self.quizzes, self.best_score)
        print("=" * 40)

    def add_quiz(self):
        """새로운 퀴즈 추가 기능[cite: 1]"""
        print("\n📌 새로운 퀴즈를 추가합니다.")
        
        question = input("문제를 입력하세요: ").strip()
        if not question:
            print("⚠️ 빈 문제는 등록할 수 없습니다.")
            return
            
        choices = []
        for i in range(1, 5):
            choice = input(f"선택지 {i}: ").strip()
            choices.append(choice)
            
        while True:
            ans_str = input("정답 번호 (1-4): ").strip()
            try:
                ans = int(ans_str)
                if 1 <= ans <= 4:
                    break
                print("⚠️ 1에서 4 사이의 숫자를 입력하세요.")
            except ValueError:
                print("⚠️ 올바른 숫자를 입력하세요.")
                
        new_quiz = Quiz(question, choices, ans)
        self.quizzes.append(new_quiz)
        
        # 파일에 즉시 저장[cite: 1]
        save_game_data(self.quizzes, self.best_score)
        print("\n✅ 퀴즈가 추가되었습니다!")

    def view_quizzes(self):
        """등록된 퀴즈 목록 확인 기능[cite: 2]"""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다.")
            return
            
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"[{idx}] {quiz.question}")
        print("-" * 40)

    def check_score(self):
        """최고 점수 확인 기능[cite: 2]"""
        print("\n" + "=" * 40)
        print(f"🏆 최고 점수: {self.best_score}점")
        print("=" * 40)

# 프로그램 실행 진입점
if __name__ == "__main__":
    game = QuizGame()
    game.run()