import subprocess

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

def main():
    tweet_text = "Swayy is a beautiful new dashboard for discovering and curating online content."

    #tweet_text = "Salman's remarks are a mockery of rape victims and their families, says Nirbhaya's mother"

    cmuTagger(tweet_text)

if __name__ == '__main__':
    main()