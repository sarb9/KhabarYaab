import hazm
import re
from ling_modules.pipline import Pipeline


class Normalizer:
    def normalize(self, text):
        compile_patterns = lambda patterns: [(re.compile(pattern), repl) for pattern, repl in patterns]

        ###
        punc_after, punc_before = r'\.:!،؛؟»\]\)\}', r'«\[\(\{'
        affix_spacing_patterns = compile_patterns([
            (r'([^ ]ه) ی ', r'\1‌ی '),  # fix ی space
            (r'(^| )(ن?می) ', r'\1\2‌'),  # put zwnj after می, نمی
            (
                r'(?<=[^\n\d ' + punc_after + punc_before + ']{2}) (تر(ین?)?|گری?|های?)(?=[ \n' + punc_after + punc_before + ']|$)',
                r'‌\1'),  # put zwnj before تر, تری, ترین, گر, گری, ها, های
            (r'([^ ]ه) (ا(م|یم|ش|ند|ی|ید|ت))(?=[ \n' + punc_after + ']|$)', r'\1‌\2'),
            # join ام, ایم, اش, اند, ای, اید, ات
        ])

        ###
        character_refinement_patterns = compile_patterns([
            (r' +', ' '),  # remove extra spaces
            (r'\n\n+', '\n\n'),  # remove extra newlines
            (r'[ـ\r]', ''),  # remove keshide, carriage returns]
            # ('"([^\n"]+)"', r'«\1»'),  # replace quotation with gyoome
            # ('([\d+])\.([\d+])', r'\1٫\2'),  # replace dot with momayez
            (r' ?\.\.\.', ' …'),  # replace 3 dots
            ('[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652]', ''),
            # remove FATHATAN, DAMMATAN, KASRATAN, FATHA, DAMMA, KASRA, SHADDA, SUKUN
        ])

        def apply_translations(text):
            translation_src, translation_dst = ' كي“”', ' کی""'
            translation_src += '0123456789%'
            translation_dst += '۰۱۲۳۴۵۶۷۸۹٪'
            maketrans = lambda A, B: dict((ord(a), b) for a, b in zip(A, B))
            translations = maketrans(translation_src, translation_dst)
            text = text.translate(translations)
            return text

        def character_refinement(text):
            for pattern, normalized_pattern in character_refinement_patterns:
                text = pattern.sub(text, normalized_pattern)
            return text

        def fix_spacing(text):
            for pattern, normalized_pattern in affix_spacing_patterns:
                text = pattern.sub(text, normalized_pattern)
            return text

        normalization_pipeline = Pipeline(apply_translations, character_refinement, fix_spacing)
        normalization_pipeline.feed(text=text)
        return text

    def __call__(self, text):
        if isinstance(text, list):
            return [self.normalize(t) for t in text]
        else:
            return self.normalize(text)
