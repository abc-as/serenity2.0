
import openai

openai.api_key = "-----"


def get_book_recommendations(user_interests, user_genres):
    interests_text = " ".join([interest.text for interest in user_interests])
    genres = [genre.name for genre in user_genres]

    genre_prompts = {
        genre: (
            f"Based on the following interests: {interests_text}, recommend 5 books for the genre '{genre}'. "
            "Provide the book titles, author names, and a brief description, each on a new line. Format: "
            "Title: <title>, Author: <author>, Description: <description>"
        )
        for genre in genres
    }
    
    recommendations = {}
    
    for genre, prompt in genre_prompts.items():
        try:
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=300, 
                temperature=0.5
            )
            genre_books = response.choices[0].text.strip().split('\n')
            books = []
            for line in genre_books:
                parts = line.split(', ')
                if len(parts) >= 3:
                    title = parts[0].replace('Title: ', '').strip()
                    author = parts[1].replace('Author: ', '').strip()
                    description = parts[2].replace('Description: ', '').strip()
                    books.append({
                        'title': title,
                        'author': author,
                        'description': description
                    })
            recommendations[genre] = books
            print(recommendations)
        except Exception as e:
            print(f"Error for genre {genre}: {e}")
            recommendations[genre] = []

    return recommendations