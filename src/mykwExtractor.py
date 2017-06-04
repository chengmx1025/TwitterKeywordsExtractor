import nltk
import subprocess
import re

def cmuTagger(tweet_text):
    txt_file = "../data/tweets.txt"
    file_object = open(txt_file, 'w')
    file_object.write(tweet_text)
    file_object.close()

    command = "./../tools/cmu_tweet_nlp/runTagger.sh"
    arg1 = "--output-format"
    arg2 = "conll"
    arg3 = txt_file
    child = subprocess.Popen([command, arg1, arg2, arg3], stdout=subprocess.PIPE)
    out_data, err_data = child.communicate()
    #print(shell_out[0])

    tag_result = []
    lines = out_data.split('\n')
    for eachLine in lines:
        tokens = eachLine.split('\t')
        if(len(tokens)==3):
            word = tokens[0]
            tag = tokens[1]
            confidence = tokens[2]

            word_tup = (word, tag)
            tag_result.append(word_tup)

    print(tag_result)
    return tag_result


#############################################################################
# This is our semi-CFG; Extend it according to your own needs
#############################################################################
cfg = {}
cfg["N+N"] = "NI"
cfg["NI+N"] = "NI"
cfg["A+A"] = "A"
cfg["A+N"] = "NI"
cfg["^+^"] = "^"


#############################################################################
class NPExtractor(object):
    def __init__(self, sentence):
        self.sentence = sentence

    # Split the sentence into singlw words/tokens
    def tokenize_sentence(self, sentence):
        try:
            tokens = nltk.word_tokenize(sentence)
        except:
            tokens = []
        return tokens

    # Normalize brown corpus' tags ("NN", "NN-PL", "NNS" > "NN")
    def normalize_tags(self, tagged):
        n_tagged = []
        for t in tagged:
            if t[1] == "NP-TL" or t[1] == "NP":
                n_tagged.append((t[0], "NNP"))
                continue
            if t[1].endswith("-TL"):
                n_tagged.append((t[0], t[1][:-3]))
                continue
            if t[1].endswith("S"):
                n_tagged.append((t[0], t[1][:-1]))
                continue
            n_tagged.append((t[0], t[1]))
        return n_tagged

    # Extract the main topics from the sentence
    def extract(self):
        #tokens = self.tokenize_sentence(self.sentence)
        #print(tokens)

        #tags = self.normalize_tags(bigram_tagger.tag(tokens))
        #print(bigram_tagger.tag(tokens))
        #print(tags)

        tags = cmuTagger(self.sentence)

        merge = True
        while merge:
            merge = False
            for x in range(0, len(tags) - 1):
                t1 = tags[x]
                t2 = tags[x + 1]
                key = "%s+%s" % (t1[1], t2[1])
                value = cfg.get(key, '')
                if value:
                    merge = True
                    tags.pop(x)
                    tags.pop(x)
                    match = "%s %s" % (t1[0], t2[0])
                    pos = value
                    tags.insert(x, (match, pos))
                    break
        matches = []

        print(tags)

        for t in tags:
            #if t[1] == "NNP" or t[1] == "NNI":
            if t[1] == "^" or t[1] == "NI":
                # if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN":
                matches.append(t[0])
            if t[1] == "#":
                #print(t[0])
                a = t[0]
                a = re.sub(r'#', "", a)
                matches.append(a)

        return matches


# Main method, just run "python np_extractor.py"
def main():
    #sentence = "Swayy is a beautiful new dashboard for discovering and curating online content."
    #sentence = "Trump social media team deleted the tweet. The Internet never forgets you morons."
    #sentence = ""

    sentence = "My workspace, having flowers on my table always boost my creativity. I love white Tulips. #design #workspace "

    np_extractor = NPExtractor(sentence)
    result = np_extractor.extract()
    print("This sentence is about: %s" % ", ".join(result))

if __name__ == '__main__':
    main()