export class Movie {
    constructor(
        public title: string,
        public year: number,
        public runtime: number,
        public mov_rel_dt:  Date,
        public mov_plot: string,
        public aname: string[],
        public dname: string,
        public wname: string[],
    ) { }
}


