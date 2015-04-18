import matplotlib.pyplot as plt

ROLE_COLORS = {"R1":"black",
               "R2":"red",
               "R3":"green",
               "R4":"blue",
               "R5":"orange",
               "R6":"purple",
               "R7":"grey",
               "NONE":"pink"}


def draw_roles(p,z,roles,background=False,marker=".",size=1):
    c = [ROLE_COLORS[x] for x in roles]
    plt.scatter(p,z,color=c,marker=marker,s=size)
    
    if background:
        ylim = plt.ylim()
        plt.hlines(2.5,0,1)
        plt.vlines(0.05,ylim[0],2.5)
        plt.vlines(0.625,ylim[0],2.5)
        plt.vlines(0.8,ylim[0],2.5)

        plt.vlines(0.3,2.5,ylim[1])
        plt.vlines(0.75,2.5,ylim[1])
        plt.fill([0,0.3,0.3,0],[ylim[1],ylim[1],2.5,2.5],color=ROLE_COLORS["R5"],alpha=.2)
        plt.fill([0.75,0.3,0.3,0.75],[ylim[1],ylim[1],2.5,2.5],color=ROLE_COLORS["R6"],alpha=.2)
        plt.fill([0.75,1,1,.75],[ylim[1],ylim[1],2.5,2.5],color=ROLE_COLORS["R7"],alpha=.2)

        plt.fill([0,.05,.05,0],[ylim[0],ylim[0],2.5,2.5],color=ROLE_COLORS["R1"],alpha=.2)
        plt.fill([.625,.05,.05,.625],[ylim[0],ylim[0],2.5,2.5],color=ROLE_COLORS["R2"],alpha=.2)
        plt.fill([.625,.8,.8,.625],[ylim[0],ylim[0],2.5,2.5],color=ROLE_COLORS["R3"],alpha=.2)
        plt.fill([1,.8,.8,1],[ylim[0],ylim[0],2.5,2.5],color=ROLE_COLORS["R4"],alpha=.2)

        plt.ylim(ylim)
        plt.xlim((-0.01,1))
        plt.xlabel("Participation coefficient")
        plt.ylabel("z-score of within-module degree")

