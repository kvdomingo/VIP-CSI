from csv import reader
from argparse import ArgumentParser
from datetime import datetime
from numpy import array, zeros
from numpy.random import seed, choice, shuffle
from pandas import date_range, Series, DataFrame


class SeminarScheduler:
    def __init__(self,
                 personlist=None,
                 taglist=None,
                 rolelist=None,
                 start_date="2020-1-20",
                 end_date="2020-5-13",
                 savename="schedule.csv",
                 rand_seed=314):

        seed(rand_seed)

        if personlist == None and taglist == None and rolelist == None:
            self.tags = []
            self.mems = []
            with open("roles.txt", encoding="utf-8") as f:
                self.roles = f.read().strip("\n").split("'")[1::2]
            with open("mems.txt", encoding="utf-8") as f:
                for mem, tag in reader(f):
                    self.mems.append(mem)
                    self.tags.append(tag)
        else:
            self.mems = personlist
            self.tags = taglist
            self.roles = rolelist

        start_date = array(start_date.split("-")).astype(int)
        start_date = datetime(*start_date)
        end_date = array(end_date.split("-")).astype(int)
        end_date = datetime(*end_date)

        self.savename = savename
        self.dates = date_range(start_date, end_date, freq="W-MON").strftime("%d-%b")
        self.seniors = [self.mems[i] for i in range(len(self.mems)) if self.tags[i] == "Senior"]
        self.juniors = [self.mems[i] for i in range(len(self.mems)) if self.tags[i] == "Junior"]
        self.org = zeros((len(self.roles), len(self.dates)), dtype="<U16")

        self.main()

    def generate_senior_speakers(self):
        pos = choice(4*len(self.dates), len(self.seniors), replace=False)
        self.org[:4].flat[pos] = self.seniors

    def generate_junior_speakers(self):
        draw_pattern = self.juniors.copy()
        shuffle(draw_pattern)
        draw = draw_pattern.copy()
        for i in range(4*len(self.dates)):
            if len(draw) == 0:
                draw = draw_pattern.copy()
            if len(self.org[:4].T.flat[i]) > 0:
                continue
            self.org[:4].T.flat[i] = draw.pop(0)

    def generate_roles(self):
        draw_pattern = self.mems.copy()
        shuffle(draw_pattern)
        draw = draw_pattern.copy()
        for i in range(4, 8):
            for j in range(len(self.dates)):
                p = 0
                if len(draw) == 0:
                    draw = draw_pattern.copy()
                while draw[p] in self.org[:,j]:
                    if p + 1 == len(draw):
                        draw.extend(draw_pattern.copy())
                    p += 1
                self.org[i,j] = draw.pop(p)

    def generate_monitors(self):
        draw_pattern = self.juniors.copy()
        shuffle(draw_pattern)
        draw = draw_pattern.copy()
        for i in range(8, len(self.roles)):
            for j in range(len(self.dates)):
                p = 0
                if len(draw) == 0:
                    draw = draw_pattern.copy()
                while draw[p] in self.org[:,j]:
                    if p + 1 == len(draw):
                        draw.extend(draw_pattern.copy())
                    p += 1
                self.org[i,j] = draw.pop(p)

    def make_df(self, **kwargs):
        self.df = DataFrame(data=self.org,
                            index=self.roles,
                            columns=self.dates,
                            dtype=str,
                            **kwargs)

    def save(self):
        self.df.to_csv(self.savename, index=False)

    def main(self):
        self.generate_senior_speakers()
        self.generate_junior_speakers()
        self.generate_roles()
        self.generate_monitors()
        self.make_df()


def main():
    parser = ArgumentParser()
    parser.add_argument("-sdl", "--start-date", help="Starting date")
    parser.add_argument("-edl", "--end-date", help="Ending date")
    parser.add_argument("-rs", "--random-seed", help="Random seed")
    parser.add_argument("-f", "--filename", help="Name of file to save to")
    args = parser.parse_args()
    args_dict = dict()

    if args.start_date:
        args_dict["start_date"] = args.start_date
        print(f"Start date: {args.start_date}")
    if args.end_date:
        args_dict["end_date"] = args.end_date
        print(f"End date: {args.end_date}")
    if args.random_seed:
        args_dict["rand_seed"] = int(args.random_seed)
        print(f"Random seed: {args.random_seed}")
    if args.filename:
        args_dict["savename"] = args.filename
        print(f"Savename: {args.filename}")

    args_dict["personlist"] = []
    args_dict["taglist"] = []
    with open("roles.txt", encoding="utf-8") as f:
        args_dict["rolelist"] = f.read().strip("\n").split("'")[1::2]
    with open("mems.txt", encoding="utf-8") as f:
        for mem, tag in reader(f):
            args_dict["personlist"].append(mem)
            args_dict["taglist"].append(tag)
    sched = SeminarScheduler(**args_dict)
    sched.make_df()
    sched.save()
    print(sched.df)
    print(f"DataFrame saved to {sched.savename}")


if __name__ == '__main__':
    main()
