from jokes import get_joke_by_type


def main():
    joke_type = input("Enter the type of joke you want (Programming/Dark/Pun/...): ")
    joke = get_joke_by_type(joke_type)

    print("Here's your joke:")
    print(joke)


if __name__ == "__main__":
    main()
