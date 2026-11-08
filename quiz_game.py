import json
import os
from quiz import Quiz
from default_quizzes import get_default_quizzes

DATA_FILE = "state.json"

class QuizGame:
    def __init__(self):
        self.quizzes, self.best_score, self.history = self.load_game_data()

    def load_game_data(self):
        """파일에서 퀴즈 목록, 최고 점수, 기록 히스토리를 불러오는 함수"""
        if not os.path.exists(DATA_FILE):
            return get_default_quizzes(), 0, []

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
            return get_default_quizzes(), 0, []

    def save_game_data(self):
        """게임 데이터를 JSON 파일에 저장하는 함수"""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
            "history": self.history
        }
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"⚠️ 데이터 파일 저장 오류 발생: {e}")

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
        self.save_game_data()
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
                    self.save_game_data()
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