from difflib import SequenceMatcher
import math

class Similarity(object):
	"""docstring for Similarity."""
	def __init__(self, limit=0.8):
		self.limit = limit

	def getScore(self, str1, str2, limit=0.8):

		score_diff = 1
		if(str1 != str2):
			str1_score = self.getScore(str1, str1, self.limit)[2]
			str2_score = self.getScore(str2, str2, self.limit)[2]
			score_diff = abs(str1_score-str2_score) if abs(str1_score-str2_score) != 0 else 1

		interests = str1.split(" ")
		keywords = str2.split(" ")

		s = SequenceMatcher(None)
		seq_score = 0
		nb_match = 0
		score = 0
		for interest in interests:
			s.set_seq2(interest)
			for keyword in keywords:
				s.set_seq1(keyword)
				b = s.ratio()>=self.limit and len(s.get_matching_blocks())==2
				seq_score += s.ratio()
				if b:
					nb_match += 1
		score = math.pow(nb_match, 5) * seq_score
		similarity = round(score*nb_match/score_diff)
		is_similar = similarity >= 1

		return (seq_score, nb_match, score, score_diff, similarity, is_similar)

	def isSimilar(self, str1, str2):
		if(str1.find(str2) != -1 or str2.find(str1) != -1):
			return True
		return self.getScore(str1, str2)[5]
