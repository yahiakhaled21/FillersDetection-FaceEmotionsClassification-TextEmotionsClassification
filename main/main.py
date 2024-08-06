import sys
import os

def main(video_path):
    subfolder_path = os.path.join(os.path.dirname(__file__), 'Scripts')
    sys.path.append(subfolder_path)

    import Text_Emotions_Classifier
    import Face_Emotions_Classifier
    import Fillers_Detection

    score_Text_Emotions_Classifier = 0
    score_Face_Emotions_Classifier = 0
    score_Fillers_Detection = 0
    final_score = 0

    #######################################################

    result_Text_Emotions_Classifier = Text_Emotions_Classifier.main(video_path)

    if result_Text_Emotions_Classifier is not None:
        score_Text_Emotions_Classifier = result_Text_Emotions_Classifier
        print(f"Score for Text Emotions Classifier is: {score_Text_Emotions_Classifier}")
        final_score += score_Text_Emotions_Classifier
    else:
        print("Error processing video in Text_Emotions_Classifier.py")

    ########################################################

    result_Face_Emotions_Classifier = Face_Emotions_Classifier.main(video_path)

    if result_Face_Emotions_Classifier is not None:
        score_Face_Emotions_Classifier = result_Face_Emotions_Classifier
        print(f"Score for Face Emotions Classifier is: {score_Face_Emotions_Classifier}")
        final_score += score_Face_Emotions_Classifier
    else:
        print("Error processing video in Face_Emotions_Classifier.py")

    ########################################################

    result_Fillers_Detection = Fillers_Detection.main(video_path)

    if result_Fillers_Detection is not None:
        score_Fillers_Detection = result_Fillers_Detection
        print(f"Score for Fillers Detection Classifier is: {score_Fillers_Detection}")
        final_score += score_Fillers_Detection
    else:
        print("Error processing video in Fillers_Detection.py")

    print("Calculating Final Score...")
    print(f"Final Score is:  {final_score}")

    return final_score  # Return the final score
