from quiz_game import QuizGame
from quiz_play import play_quiz

def display_menu():
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

def main():
    game = QuizGame()

    try:
        while True:
            display_menu()
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
                play_quiz(game)
            elif choice == 2:
                game.add_quiz()
            elif choice == 3:
                game.delete_quiz()
            elif choice == 4:
                game.view_quizzes()
            elif choice == 5:
                game.check_score_and_history()
            elif choice == 6:
                print("\n👋 프로그램을 종료합니다. 감사합니다!")
                break
                
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 프로그램이 강제 중단되었습니다. 안전하게 저장 후 종료합니다.")
        game.save_game_data()

if __name__ == "__main__":
    main()