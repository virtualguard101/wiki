all: gp pa mp pipe rps

gp: getProcess.c
	gcc -o getprocess getProcess.c

pa: processArray.c
	gcc -o processarray processArray.c

mp: multi-processes.c
	gcc -o multiprocess multi-processes.c

pipe: pipe.c
	gcc -o pipe pipe.c

rps: rps.c
	gcc -o rps rps.c

clean:
	rm -f getprocess processarray multiprocess pipe rps