import json
import os
import random
from datetime import datetime

DATA_FILE = "state.json"

class Quiz:
    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint  # 💡 보너스 3: 힌트 속성

    def check_answer(self, user_answer):
        return self.answer == user_answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint
        }

def load_game_data():
    """파일에서 퀴즈 목록, 최고 점수, 기록 히스토리를 불러오는 함수"""
    if not os.path.exists(DATA_FILE):
        # 회원님이 직접 만드신 센스 있는 5문제와 힌트 설정
        default_quizzes = [
            Quiz("다음 중 가장 성격이 나쁜 강아지는?", ["골든 리트리버", "시츄", "치와와", "사모예드"], 3, "작고 눈이 똥그란 소형견입니다."),
            Quiz("성심당에서 팔지 않는 것은?", ["명란 바게트", "튀김 소보로", "딸기시루", "한방능이백숙"], 4, "빵집에서 보양식을 팔 리 없겠죠?"),
            Quiz("빛의 삼원색이 아닌 것은?", ["노랑", "빨강", "파랑", "초록"], 1, "물감의 삼원색과 헷갈리지 마세요!"),
            Quiz("대전 출신이 아닌 연예인은?", ["설윤", "안유진", "카리나", "조보아"], 3, "나머지 세 명은 대전과 깊은 연이 있습니다."),
            Quiz("\"낮말은 새가 듣고 밤말은 o가 듣는다\" 여기서 o는?", ["공룡", "문어", "쥐", "개"], 3, "벽에 구멍이 있으면 누가 들을까요?")
        ]
        return default_quizzes, 0, []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            quizzes = []
            for q in data.get("quizzes", []):
                quizzes.append(Quiz(
                    q.get("question"),
                    q.get("choices"),
                    q.get("answer"),
                    q.get("hint", "힌트 없음")
                ))
            best_score = data.get("best_score", 0)
            history = data.get("history", [])
            return quizzes, best_score, history
    except Exception as e:
        print(f"⚠️ 데이터 파일 읽기 오류 발생: {e}. 기본 데이터를 사용합니다.")
        return [], 0, []

def save_game_data(quizzes, best_score, history):
    """게임 데이터를 JSON 파일에 저장하는 함수"""
    data = {
        "quizzes": [q.to_dict() for q in quizzes],
        "best_score": best_score,
        "history": history
    }
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"⚠️ 데이터 파일 저장 오류 발생: {e}")

class QuizGame:
    def __init__(self):
        self.quizzes, self.best_score, self.history = load_game_data()

    def display_menu(self):
        """메뉴 화면 출력"""
        print("\n" + "=" * 40)
        print("        🎯 나만의 퀴즈 게임 (보너스 포함) 🎯        ")
        print("=" * 40)
        print("1. 퀴즈 풀기 (랜덤 & 문제 수 선택 & 힌트)")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 삭제")
        print("4. 퀴즈 목록")
        print("5. 점수 및 히스토리 확인")
        print("6. 종료")
        print("=" * 40)

    def run(self):
        """메인 실행 루프"""
        try:
            while True:
                self.display_menu()
                choice_str = input("선택: ").strip()
                
                if not choice_str:
                    print("⚠️ 잘못된 입력입니다. 1-6 사이의 숫자를 입력하세요.")
                    continue
                    
                try:
                    choice = int(choice_str)
                except ValueError:
                    print("⚠️ 잘못된 입력입니다. 1-6 사이의 숫자를 입력하세요.")
                    continue
                    
                if choice < 1 or choice > 6:
                    print("⚠️ 잘못된 입력입니다. 1-6 사이의 숫자를 입력하세요.")
                    continue
                    
                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.delete_quiz()
                elif choice == 4:
                    self.view_quizzes()
                elif choice == 5:
                    self.check_score_and_history()
                elif choice == 6:
                    print("\n👋 프로그램을 종료합니다. 감사합니다!")
                    break
                    
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 프로그램이 강제 중단되었습니다. 안전하게 저장 후 종료합니다.")
            save_game_data(self.quizzes, self.best_score, self.history)

    def play_quiz(self):
        """퀴즈 풀기 (랜덤 출제, 문제 수 선택, 힌트 및 점수 차감)"""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해주세요!")
            return
            
        total_available = len(self.quizzes)
        print(f"\n📝 퀴즈를 시작합니다! (등록된 총 문제 수: {total_available}개)")
        
        while True:
            cnt_str = input(f"풀고 싶은 문제 수를 입력하세요 (1 ~ {total_available}): ").strip()
            try:
                num_questions = int(cnt_str)
                if 1 <= num_questions <= total_available:
                    break
                print(f"⚠️ 1에서 {total_available} 사이의 숫자를 입력하세요.")
            except ValueError:
                print("⚠️ 올바른 숫자를 입력하세요.")

        selected_quizzes = random.sample(self.quizzes, num_questions)
        correct_weighted_score = 0
        
        for idx, quiz in enumerate(selected_quizzes, 1):
            print("\n" + "-" * 40)
            print(f"[문제 {idx}/{num_questions}]")
            print(quiz.question)
            for i, choice in enumerate(quiz.choices, 1):
                print(f"{i}. {choice}")
                
            hint_used = False
            
            while True:
                ans_input = input("\n정답 번호 입력 (1~4) 또는 힌트 보기 ('h'): ").strip().lower()
                
                if ans_input == 'h':
                    if not hint_used:
                        print(f"💡 [힌트]: {quiz.hint}")
                        hint_used = True
                    else:
                        print("⚠️ 이미 이 문제에서 힌트를 사용하셨습니다!")
                    continue
                    
                if not ans_input:
                    print("⚠️ 빈 입력입니다. 숫자를 입력하거나 'h'를 입력하세요.")
                    continue
                    
                try:
                    ans = int(ans_input)
                    if ans < 1 or ans > 4:
                        print("⚠️ 1~4 사이의 숫자를 입력하세요.")
                        continue
                    break
                except ValueError:
                    print("⚠️ 숫자 또는 'h'를 입력해주세요.")
                    
            if quiz.check_answer(ans):
                print("✅ 정답입니다!")
                if hint_used:
                    print("   (⚠️ 힌트를 사용하여 해당 문제는 0.5점 처리됩니다.)")
                    correct_weighted_score += 0.5
                else:
                    correct_weighted_score += 1.0
            else:
                print(f"❌ 틀렸습니다! 정답은 {quiz.answer}번입니다.")
                
        score = int((correct_weighted_score / num_questions) * 100)
        
        print("\n" + "=" * 40)
        print(f"🏆 결과: {num_questions}문제 중 맞춘 점수 환산 {score}점")
        print("=" * 40)
        
        if score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수 달성!")

        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_record = {
            "date": now_time,
            "total": num_questions,
            "score": score
        }
        self.history.append(history_record)
        save_game_data(self.quizzes, self.best_score, self.history)

    def add_quiz(self):
        """새로운 퀴즈 추가 (힌트 포함)"""
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
                
        hint = input("문제의 힌트를 입력하세요: ").strip()
        if not hint:
            hint = "힌트 없음"

        new_quiz = Quiz(question, choices, ans, hint)
        self.quizzes.append(new_quiz)
        save_game_data(self.quizzes, self.best_score, self.history)
        print("\n✅ 퀴즈가 성공적으로 추가되었습니다!")

    def delete_quiz(self):
        """퀴즈 삭제 기능"""
        if not self.quizzes:
            print("\n⚠️ 삭제할 퀴즈가 없습니다.")
            return
            
        print(f"\n🗑️ 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"[{idx}] {quiz.question}")
        print("-" * 40)
        
        while True:
            del_str = input("삭제할 퀴즈 번호를 입력하세요 (취소하려면 0): ").strip()
            try:
                del_idx = int(del_str)
                if del_idx == 0:
                    print("취소되었습니다.")
                    return
                if 1 <= del_idx <= len(self.quizzes):
                    removed = self.quizzes.pop(del_idx - 1)
                    save_game_data(self.quizzes, self.best_score, self.history)
                    print(f"\n✅ '{removed.question}' 퀴즈가 삭제되었습니다!")
                    break
                print("⚠️ 올바른 번호를 입력하세요.")
            except ValueError:
                print("⚠️ 숫자로 입력해주세요.")

    def view_quizzes(self):
        """퀴즈 목록 확인"""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다.")
            return
            
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"[{idx}] {quiz.question} (힌트: {quiz.hint})")
        print("-" * 40)

    def check_score_and_history(self):
        """최고 점수 및 전체 게임 히스토리 확인"""
        print("\n" + "=" * 40)
        print(f"🏆 현재 최고 점수: {self.best_score}점")
        print("=" * 40)
        
        if not self.history:
            print("📜 아직 플레이 기록이 없습니다.")
            return
            
        print(f"\n📜 전체 게임 플레이 히스토리 (총 {len(self.history)}회)")
        print("-" * 50)
        for idx, h in enumerate(self.history, 1):
            print(f"{idx}. 일시: {h['date']} | 푼 문제 수: {h['total']}문제 | 점수: {h['score']}점")
        print("-" * 50)

if __name__ == "__main__":
    game = QuizGame()
    game.run()

    