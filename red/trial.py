import time
import typer
from datetime import datetime
from devices import DEMUX, DISTS
from sa import MyRow, SESSION_MyRow, MyDist, SESSION_MyDist


def loop_demux(demuxer_a):
    global SESSION_MyRow
    for cur_ind in demuxer_a.connect_inds:
        start = datetime.utcnow()
        demuxer_a.run_select(cur_ind)
        stop = datetime.utcnow()
        cur_entry = MyRow(index=cur_ind, start=start, stop=stop)
        cur_entry.add(SESSION_MyRow)
        # rest between each
        time.sleep(0.5)


def loop_dist(dists):
    global SESSION_MyDist
    UNIT = "in"
    PRECISION = 4
    out = []
    for cur_ind in dists.connect_inds:
        cur_v = dists.obtain_reading(cur_ind, precision=PRECISION, unit=UNIT)
        cur_entry = MyDist(index=cur_ind, value=cur_v, unit=UNIT)
        cur_entry.add(SESSION_MyDist)
        out.append((cur_ind, cur_v))
    return out


def main(loops: int = 10):

    # init
    time.sleep(1)

    # main loop
    try:
        for i in range(loops):
            # demuxer_a
            loop_demux(DEMUX)
            print("done demuxer_a")

            # dist
            ret_val = loop_dist(DISTS)
            print(f"dists: {ret_val}")

            time.sleep(2)

    except KeyboardInterrupt:
        DEMUX.zero()
        print("demuxer_a zeroed")


if __name__ == "__main__":
    typer.run(main)