# Ling571 HW6 FCFG
import sys
import nltk


def make_grammar(grammar):

    # Make grammar
    fcfg = nltk.data.load(grammar)
    # Create parser
    parser = nltk.parse.FeatureChartParser(fcfg)

    return parser


def output_result(r, sentence, out_file):
    with open(out_file, 'a', encoding='utf8') as f:
        f.write(f'{sentence}')
        f.write(f'{r}\n')

            


if __name__=="__main__":
    try:
        grammar_f = sys.argv[1]
        sentences = sys.argv[2]
        output_f = sys.argv[3]

        # Create parser
        parser = make_grammar(grammar_f)

        # Read in sentences
        with open(sentences, 'r', encoding='utf8') as f:
            sents = f.readlines()
            # print(sents)
            for sent in sents:
                # Tokenize
                words = nltk.word_tokenize(sent)

                # Parse and output result
                parsed = parser.parse(words)

                for parse in parsed:
                    # Only generate one parse
                    result = parse.label()['SEM'].simplify()
                    output_result(result, sent, output_f)
                    break

    
    
    except OSError as e:
        print(e)

    