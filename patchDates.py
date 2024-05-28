import datetime

# The dates for every major patch, so that we can potentially combine all jcg results from a
# particular patch
SRinitial = datetime.datetime(2019,3,27)
SRmini = datetime.datetime(2019,5,20)
RoGinitial = datetime.datetime(2019,6,26)
RoGVNerf = datetime.datetime(2019,7,10)
RoGBuffs = datetime.datetime(2019,7,29)
RoGmini = datetime.datetime(2019,8,22)
VRinitial = datetime.datetime(2019,9,25)
VRNerf = datetime.datetime(2019,10,29)
UCinitial = datetime.datetime(2019,12,28)
Premini = datetime.datetime(2020,2,2)
DoVPre = datetime.datetime(2021,4,1)
DovMini = datetime.datetime(2021,5,19)
RenaPre = datetime.datetime(2021,6,28)
RenaNerf = datetime.datetime(2021,7,7)
DoCNerf = datetime.datetime(2022,1,7)
Festive = datetime.datetime(2022,3,25)
RoG = datetime.datetime(2022,6,28)
RoGNerf = datetime.datetime(2022,7,6)
Convict = datetime.datetime(2023,1,1)
AzvaldtMini = datetime.datetime(2023,2,20)
Academy = datetime.datetime(2023,3,27)
AcademyNerf = datetime.datetime(2023,3,30)
AcademyBuff = datetime.datetime(2023,4,23)
HeroesMini = datetime.datetime(2024,5,20)

# A list of the dates that each patch went live along with a descriptive name
dates = [[SRinitial, "Steel Rebellion Initial"],
        [UCinitial, "UC initial"],
        [DoVPre, "DoV, pre-mini"],
        [DovMini, "DoV, mini"],
        [RenaPre, "Rena, pre-mini"],
        [RenaNerf, "Rena, post-nerf"],
        [DoCNerf, "DoC, post-nerf"],
        [Festive, "Festive"],
        [RoG, "RoG"],
        [RoGNerf, "RoGNerf"],
        [Convict, "Convict"],
        [AzvaldtMini, "Azvaldt Mini"],
        [Academy, "Academy"],
        [AcademyNerf, "Academy Nerf"],
        [AcademyBuff, "Academy Buff"],
        [HeroesMini, "Heroes mini"]
        ]

