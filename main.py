import matplotlib.pyplot as plt



amin = 0.2
amax = 1.3
astep = 0.1
C = 20 #pojemnosc systemu
M = 2 # liczba strumieni
ti = [1, 3] #liczba AU wymagana przez jedną klase strumienia



def var_input():
    global amin, amax, astep, C, M, ti
    amin = float(input("Enter amin: "))
    amax = float(input("Enter amax: "))
    astep = float(input("Enter astep: "))
    C = int(input("Enter C: "))
    M = int(input("Enter M: "))
    ti = [0 for i in range(M)]
    for i in range(M):
        ti[i] = int(input("Enter ti["+ str(i) +"]: "))

def write_header(filename):
    with open(filename, "w") as f:
        f.write("# C = " + str(C) + '\n')
        f.write("#\n")
        for i in range(len(ti)):
            f.write("#      t[" + str(i+1) + "] = " + str(ti[i]) + "\n")
        f.write("#\n")
    f.close()

def write_data1(filename, array):
    with open(filename, "a") as f:
        f.write("a      ")
        for i in range(len(ti)):
            f.write("t" + str(i+1))
            for k in range(len(str(array[1][1]))+8):
                f.write(" ")
        f.write("\n")
        for i in range(len(array)):
            f.write(str(round(amin+astep*i, 1)) + "    ")
            for j in range(len(ti)):
                f.write(str(array[i][j]))
                for k in range(len(str(array[1][1]))+10 - len(str(array[i][j]))):
                    f.write(" ")
            f.write("\n")
    f.close()
def write_data2(filename, array, a):
    with open(filename, "a") as f:
        f.write("\n" + str(round(a/10, 1)) + "\n")
        f.write("n     ")
        for i in range(len(ti)):
            f.write("t" + str(i + 1) + "        ")
        f.write(":     sum\n")
        for i in range(len(array)):
            f.write(str(i))
            for j in range(6 - len(str(i))):
                f.write(" ")
            for j in range(len(ti)):
                f.write(str(round(array[i][j], 4)))
                for k in range(10 - len(str(round(array[i][j], 4)))):
                    f.write(" ")

            f.write(":     " + str(round(sum(array[i]), 0)) +"\n")
    f.close()
def plot_file(filename):
    fti=[]
    f=open(filename, 'r')
    row = f.readline().split()
    cf = int(row[3])
    next(f)
    for i in range(M):
        row=f.readline().split()
        fti.append(int(row[3]))
    #data = f.readlines()[6:]
    next(f)
    next(f)
    data = f.readlines()
    for i in range(len(fti)):
        x = []
        y = []
        for row in data:
            row = row.split()
            x.append(float(row[0]))
            y.append(float(row[i+1]))
        plt.plot(x, y, label="t[" + str(i+1) + "]=" + str(fti[i]))
    plt.legend()
    plt.grid()
    plt.title("C=" + str(cf))
    plt.xlabel("Ruch oferowany na pojedyńczy AU")
    plt.ylabel("Prawdopodobieństwo blokady")
    plt.yscale("log")
    plt.show()
def calc_avg_reports(ai,ti, pn,n):
    if 0 <= n-ti <= C:
        return ai * ti * pn[n-ti]/pn[n]
    else:
        return 0
def calc_ai(a, i):
    return (a * C)/(M *ti[i])
def calc_ei(ti, pn):
    Ei = 0
    for n in range(C-ti+1, C+1):
        Ei = pn[n] + Ei
    return Ei
def sn_func(a):
    sn = [1]  # rozkład zajetosci
    pn = []  # prawdopodobienstwo zajetosci
    for n in range(1,C+1):
        snb = [0 for i in range(M)]  # bufor
        for i in range(M):
            if n - ti[i-1] >= 0:
                snb[i]=calc_ai(a/10, i) * ti[i] * sn[n-ti[i-1]]
        sn.append(1/n*sum(snb))

    for i in range(0,C+1):
        pn.append(sn[i]/sum(sn))
    for i in range(M):
        block_prob[int(a- 10*amin)][i] = calc_ei(ti[i], pn)
    for n in range(0,C+1):
        for i in range(0,M):
            avg_au_occupied_for_a[n][i] = calc_avg_reports(calc_ai(a/10, i),ti[i],pn, n)
    write_data2(filename2, avg_au_occupied_for_a, a)





#main
var_input()  # wartosci z terminala
ei=[0 for i in range(len(ti))]
block_prob=[[0 for i in range(len(ti))] for j in range(int(10*amin), int(10*amax)+1, int(10*astep))]
avg_au_occupied_for_a=[[0 for i in range(len(ti))] for j in range (C +1)]
filename = "C"+str(C)+"M" + str(M)
filename1 = filename + "_blockade.txt"
filename2= filename + "_au_occupied.txt"
write_header(filename1)
write_header(filename2)
for i in range(int(10*amin), int(10*amax)+1, int(10*astep)):
    sn_func(i)
write_data1(filename1, block_prob)
plot_file(filename1)


