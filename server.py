"""
Flask application to analyze emotions in user-submitted text.
Provides an endpoint '/emotionDetector' that returns emotion scores
and dominant emotion, handling blank inputs gracefully.
"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("emotionDetector")


@app.route("/emotionDetector")
def emotion_analyzer():
    """
    Flask route that processes user input text and returns emotion analysis.

    Retrieves the text from the query parameter 'textToAnalyze'.
    Calls the 'emotion_detector' function to analyze emotions.
    Returns a formatted string with emotion scores and dominant emotion.
    If the input is blank or invalid, returns an error message.

    Returns:
        str: Formatted emotion analysis or error message.
    """
    text_to_analyze = request.args.get("textToAnalyze", "")

    # Call emotion_detector function
    response_dict = emotion_detector(text_to_analyze)

    # Handle invalid input or blank text
    if response_dict["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    # Extract individual emotions
    emotions = {key: response_dict[key] for key in ["anger", 
                                                    "disgust", "fear", "joy", "sadness"]}
    dominant_emotion = response_dict["dominant_emotion"]

    # Format the response for display
    formatted_response = (
        f"For the given statement, the system response is "
        f"'anger': {emotions['anger']}, "
        f"'disgust': {emotions['disgust']}, "
        f"'fear': {emotions['fear']}, "
        f"'joy': {emotions['joy']}, "
        f"'sadness': {emotions['sadness']}. "
        f"The dominant emotion is {dominant_emotion}."
    )

    return formatted_response


@app.route("/")
def render_index_page():
    """
    Flask route that renders the index page.

    Returns:
        str: Rendered HTML page.
    """
    return render_template("index.html")


if __name__ == "__main__":
    # Run the Flask application
    app.run(host="0.0.0.0", port=5000)
