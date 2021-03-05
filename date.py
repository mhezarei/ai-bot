from utility import *


class Date:
	def __init__(self, base: str, target: str, date: str,
	             occasion: str = ""):
		self.base = base
		self.target = target
		self.date = date
		self.y, self.m, self.d = split_date(date)
		self.occasion = occasion
	
	def get_occasion_date(self):
		p = os.path.dirname(os.path.abspath(__file__))
		f = os.path.join(p, "shamsi_events.csv")
		df = pd.read_csv(f, encoding="utf-8")
		temp = df[df["event"].str.contains(self.occasion)]
		shamsi_date = convert_date(self.date, self.base, "shamsi")
		y, m, d = map(int, split_date(shamsi_date))
		ans = temp[temp["year"] == y].iloc[0]
		date = datetime(year=ans["year"],
		                month=ans["month"],
		                day=ans["day"]).strftime("%Y-%m-%d")
		return date
