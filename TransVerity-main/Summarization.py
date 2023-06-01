import spacy
from spacy.lang.en.stop_words import STOP_WORDS
# Stop words woh word h jinko hata diya toh sentence ke meaning ko farak nhi padega.
from string import punctuation
from heapq import nlargest
import requests


text = """Wikipedia[note 3] is a multilingual free online encyclopedia written and maintained by a community of volunteers, known as Wikipedians, through open collaboration and using a wiki-based editing system called MediaWiki. Wikipedia is the largest and most-read reference work in history.[3] It is consistently one of the 10 most popular websites ranked by Similarweb and formerly Alexa; as of 2023, Wikipedia was ranked the 5th most popular site in the world according to Semrush.[4] It is hosted by the Wikimedia Foundation, an American non-profit organization funded mainly through donations.

Wikipedia was launched by Jimmy Wales and Larry Sanger on January 15, 2001. Sanger coined its name as a blend of wiki and encyclopedia. Wales was influenced by the "spontaneous order" ideas associated with Friedrich Hayek and the Austrian School of economics after being exposed to these ideas by the libertarian economist Mark Thornton.[5] Initially available only in English, versions in other languages were quickly developed. Its combined editions comprise more than 60 million articles, attracting around 2 billion unique device visits per month and more than 15 million edits per month (about 5.7 edits per second on average) as of January 2023.[6][7] In 2006, Time magazine stated that the policy of allowing anyone to edit had made Wikipedia the "biggest (and perhaps best) encyclopedia in the world".[8]"""


# print(stopwords)


def summarizer(rawdoc,sel_lang,targ_lang,percent):
    def translate_text(text, source_lang, target_lang):
        base_url = "https://api.mymemory.translated.net/get"
        results = []
        for i in range(0, len(text), 500):
            chunk = text[i:i+500]
            params = {
                "q": chunk,
                "langpair": f"{source_lang}|{target_lang}"
            }
            response = requests.get(base_url, params=params)
            translation = response.json()["responseData"]["translatedText"]
            results.append(translation)
        return " ".join(results)

    text = rawdoc
    source_lang = sel_lang
    target_lang = "en"
    translated_text = translate_text(text, source_lang, target_lang)
    stopwords = list(STOP_WORDS)
    # Taking input from nlp
    
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(translated_text)
    # print(doc)

    # Tokenization of words
    tokens = [token.text for token in doc]
    # print(tokens)

    # Word frequency after neglecting stop words and punctuation
    word_freq={}

    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    # print(word_freq)

    # Checking maximum frequency of word in doc
    max_freq = max(word_freq.values())
    # print(max_freq)

    # Dividing the max frequency with all frequency to normalize the frequency
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    # Tokenization of sentences
    sent_tokens = [sent for sent in doc.sents]
    # print(sent_tokens)


    # Sentence frequency
    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]   
    # print(sent_scores)


    # It decides the percentage of summarization, here it is 30% percent
    select_len = int(len(sent_tokens) * float(percent))


    # List of summarized text that is done in order of higher frequency of sentences
    summary = nlargest(select_len, sent_scores, sent_scores.get)
    # print(summary)


    # Converting summarized list into summarized para
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    
    text = summary
    source_lang = "en"
    target_lang = targ_lang
    translated_text = translate_text(text, source_lang, target_lang)
    
    return translated_text

# document1 ="""भारत दक्षिण एशिया में स्थित एक विशाल और विविध देश है। 1.3 बिलियन से अधिक लोगों की आबादी के साथ, यह दुनिया का दूसरा सबसे अधिक आबादी वाला देश है, और यह भूमि क्षेत्र के हिसाब से सातवां सबसे बड़ा देश भी है। भारत अपने समृद्ध इतिहास, विविध संस्कृति और आश्चर्यजनक प्राकृतिक सुंदरता के लिए जाना जाता है।
# भारत का एक लंबा और जटिल इतिहास है जो हजारों साल पहले का है। देश पर सदियों से कई अलग-अलग साम्राज्यों और साम्राज्यों का शासन रहा है, प्रत्येक ने देश की संस्कृति और परंपराओं पर अपनी अनूठी छाप छोड़ी है। भारत का इतिहास ब्रिटिश औपनिवेशिक शासन से स्वतंत्रता के लिए उसके संघर्ष की विशेषता भी है, जिसे 1947 में हासिल किया गया था।
# ।आज, भारत सरकार की एक संघीय प्रणाली के साथ एक लोकतांत्रिक देश है। यह 2,000 से अधिक जातीय समूहों और 1,600 से अधिक भाषाओं का घर है, जो इसे दुनिया के सबसे विविध देशों में से एक बनाता है। भारत में हिंदू धर्म सबसे बड़ा धर्म है, लेकिन यह देश मुसलमानों, ईसाइयों, सिखों, बौद्धों और जैनियों की बड़ी आबादी का भी घर है।
# """
# ans = summarizer(document1,"hi")
# print(ans)
