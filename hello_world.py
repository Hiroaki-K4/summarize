from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter, RegexReplaceCharFilter
from janome.tokenizer import Tokenizer as JanomeTokenizer  # sumyのTokenizerと名前が被るため
from janome.tokenfilter import POSKeepFilter, ExtractAttributeFilter
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from flask import render_template, Flask, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def main_page():
    return render_template("index.html")


@app.route("/index2", methods=["POST"])
def aaa():
    # text = POSTメソッドで渡されたものを受け取る
    # sents = summarize(text)
    text = request.form['youyakumae']
    youyakugo = summarize(text)

    return render_template("index2.html", text=text, youyakugo=youyakugo)


def summarize(text):
    sentences = [t for t in text.split('\n')]
    analyzer = Analyzer(
        [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter(r'[(\)「」、。]', ' ')],  # ()「」、。は全てスペースに置き換える
        JanomeTokenizer(),
        [POSKeepFilter(['名詞', '形容詞', '副詞', '動詞']), ExtractAttributeFilter('base_form')]  # 名詞・形容詞・副詞・動詞の原型のみ
        )

    corpus = [' '.join(analyzer.analyze(s)) + '。' for s in sentences]


    parser = PlaintextParser.from_string(''.join(corpus), Tokenizer('japanese'))

    summarizer = LexRankSummarizer()
    summarizer.stop_words = [' ']

    summary = summarizer(document=parser.document, sentences_count=3)

    x = ""

    for sentence in summary:

        x += sentences[corpus.index(sentence.__str__())]

    return x


if __name__ == '__main__':
    app.run(debug=True)
    # text = """アイドルグループ・日向坂46が31日、2ndシングル｢ドレミソラシド｣を7月17日にリリースすることを公式サイトで発表した。
    # この発表に先駆け、公式ツイッターでは28日から3日連続でメンバーが楽器を演奏するもなぜかうまく弾けない謎の動画がアップされ、ファンの注目を集めていた。
    # 28日にアップされた動画では、河田陽菜が得意のピアノを披露するも、なぜか「ファ」だけが押せず、困惑の表情。
    # 29日の動画では松田好花がギターを弾くも、同じく「ファ」だけが何度弾いても音が出ず、困惑したままその場を去って動画は終了。
    # 昨日30日の動画では佐々木久美がトランペットで「ファ」の音が出ないことを佐々木を弾いてみたものの、やはり「ファ」の音だけが出ず、｢この世界から“ファ”が消えた！｣と言い残して動画は終わっていた。
    # ファンの間では「ファ」が出ないことが今後の日向坂46に大きな関係があるのではないかと憶測を呼んでいたが、きょう31日正午に2ndシングル｢ドレミソラシド｣のリリースを発表。
    # “ファ”が抜けているタイトルの発表で、3日間の動画に対する謎が解明した。
    # 日向坂46は2月に「けやき坂46」から改名し、3月のデビューシングル「キュン」では初週47.6万枚を売り上げ、オリコン週間シングルランキング初登場1位。
    # 欅坂46が記録していた「女性アーティストの1stシングルによる初週売上枚数」を抜いて歴代1位となるなど、快進撃を果たしている。"""
    # result = summarize(text)
    # print(result)