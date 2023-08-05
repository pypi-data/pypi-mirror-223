use ndarray::Zip;
use ndarray::prelude::*;


pub fn cost_scalar(
    usage: ArrayView2<f64>,
    prices: ArrayView2<f64>,
    levels: ArrayView1<f64>,
    dump: &mut Array2<f64>) -> f64 {
    let od_price = prices.slice(s![0, ..]);
    let sp_price = prices.slice(s![1, ..]);
    let ri_price = prices.slice(s![2, ..]);
    let reservations = levels.slice(s![1..]);
    let s = levels[0];
    let timespan = usage.nrows();

    let mut cost = (&reservations * &ri_price).sum() + s;
    cost *= 24. * timespan as f64;
    
    *dump = &usage - &reservations;
    (*dump).mapv_inplace(|d| if d < 0. {0.} else {d});
    
    let mut s: ArrayBase<ndarray::OwnedRepr<f64>, Dim<[usize; 1]>> = Array::ones(timespan) * s * 24.;
    for i in 0..usage.ncols() {
        let ss = &s / sp_price[i];
        let mut col_i: ArrayBase<ndarray::ViewRepr<&mut f64>, Dim<[usize; 1]>> = (*dump).column_mut(i);
        let mut min = col_i.to_owned();
        Zip::from(&mut min).and(&ss).for_each(|z, &y| {*z = z.min(y)});

        col_i -= &min;
        min *= sp_price[i];
        s -= &min;
    };

    *dump *= &od_price;

    cost + dump.sum()
}


pub fn cost_memoized(usage: ArrayView2<f64>, prices: ArrayView2<f64>, levels: ArrayView2<f64>, dump: &mut Array2<f64>) -> f64 {
    let od_price = prices.slice(s![0, ..]);
    let sp_price = prices.slice(s![1, ..]);
    let ri_price = prices.slice(s![2, ..]);
    let reservations = levels.slice(s![.., 1..]);
    let mut s = levels.slice(s![.., 0]).to_owned();

    let cost = (&reservations * &ri_price).sum() + s.sum();
    
    *dump = &usage - &reservations;
    (*dump).mapv_inplace(|d| if d < 0. {0.} else {d});
    
    for i in 0..usage.ncols() {
        let ss = &s / sp_price[i];
        let mut col_i: ArrayBase<ndarray::ViewRepr<&mut f64>, Dim<[usize; 1]>> = (*dump).column_mut(i);
        let mut min = col_i.to_owned();
        Zip::from(&mut min).and(&ss).for_each(|z, &y| {*z = z.min(y)});

        col_i -= &min;
        min *= sp_price[i];
        s -= &min;
    };

    *dump *= &od_price;

    cost + dump.sum()
}

pub fn cost(
    usage: ArrayView2<f64>,
    prices: ArrayView2<f64>,
    levels: ArrayView2<f64>,
    dump: &mut Array2<f64>)
     -> f64 {
    let od_price = prices.slice(s![0, ..]);
    let sp_price = prices.slice(s![1, ..]);
    let ri_price = prices.slice(s![2, ..]);
    let reservations = levels.slice(s![.., 1..]);
    let mut s = levels.slice(s![.., 0]).to_owned();

    let cost = (&reservations * &ri_price).sum() + s.sum();
    
    *dump = &usage - &reservations;
    (*dump).mapv_inplace(|d| if d < 0. {0.} else {d});
    
    for i in 0..usage.ncols() {
        let ss = &s / sp_price[i];
        let mut col_i: ArrayBase<ndarray::ViewRepr<&mut f64>, Dim<[usize; 1]>> = (*dump).column_mut(i);
        let mut min = col_i.to_owned();
        Zip::from(&mut min).and(&ss).for_each(|z, &y| {*z = z.min(y)});

        col_i -= &min;
        min *= sp_price[i];
        s -= &min;
    };


    *dump *= &od_price;

    cost + dump.sum()
}

pub fn coverage(
    usage: ArrayView2<f64>,
    prices: ArrayView2<f64>,
    levels: ArrayView2<f64>)
    -> f64 {


    let od_price = prices.slice(s![0, ..]);
    let sp_price = prices.slice(s![1, ..]);
    let reservations = levels.slice(s![.., 1..]);
    let mut s = levels.slice(s![.., 0]).to_owned();

    let denum = (&usage * &od_price).sum();
    let mut num = reservations.sum_axis(Axis(0)) * 24.;
    
    let mut col_i = usage.column(0).to_owned();

    for i in 0..usage.ncols() {
        let ss = &s / sp_price[i];
        col_i = 0. + &usage.column(i);
        let mut min = col_i.to_owned();
        Zip::from(&mut min).and(&ss).for_each(|z, &y| {*z = z.min(y)});

        num[i] += min.sum(); // hours of savings plans used
        min *= sp_price[i];
        s -= &min;
    };

    // ((num * od_price).sum() + s.sum()) / denum
    (num * od_price).sum() / denum

}


pub fn underutilisation(usage: ArrayView2<f64>, prices: ArrayView2<f64>, levels: ArrayView1<f64>, dump: &mut Array2<f64>) -> f64 {
    let sp_price = prices.slice(s![1, ..]);
    let ri_price = prices.slice(s![2, ..]);
    let reservations = levels.slice(s![1..]);
    let s = levels[0];
    let timespan = usage.nrows();

    let mut underutilisation = 0.;
    
    *dump = &usage - &reservations;
    underutilisation += ((*dump).mapv(|d| if d < 0. {-d} else {0.}) * ri_price).sum();
    (*dump).mapv_inplace(|d| if d < 0. {0.} else {d});
    
    let mut s: ArrayBase<ndarray::OwnedRepr<f64>, Dim<[usize; 1]>> = Array::ones(timespan) * s * 24.;
    for i in 0..usage.ncols() {
        let ss = &s / sp_price[i];
        let mut col_i: ArrayBase<ndarray::ViewRepr<&mut f64>, Dim<[usize; 1]>> = (*dump).column_mut(i);
        let mut min = col_i.to_owned();
        Zip::from(&mut min).and(&ss).for_each(|z, &y| {*z = z.min(y)});

        col_i -= &min;
        min *= sp_price[i];
        s -= &min;
    };

    underutilisation + s.sum()
}



// pub fn cost_vec(usage: ArrayView2<f64>, prices: ArrayView2<f64>, levels: ArrayView1<f64>, dump: &mut Array2<f64>) -> Array1<f64> {

//     let od_price = prices.slice(s![0, ..]);
//     let sp_price = prices.slice(s![1, ..]);
//     let ri_price = prices.slice(s![2, ..]);
//     let reservations = levels.slice(s![1..]);
//     let s = levels[0];
//     let timespan = usage.nrows();

//     let mut cost = &reservations * &ri_price * 24. * timespan as f64;
    
//     *dump = &usage - &reservations * 24.;
//     (*dump).mapv_inplace(|d| if d < 0. {0.} else {d});
    
//     let mut s: ArrayBase<ndarray::OwnedRepr<f64>, Dim<[usize; 1]>> = Array::ones(timespan) * s * 24.;
//     for i in 0..usage.ncols() {
//         let ss = &s / sp_price[i];
//         let mut col_i: ArrayBase<ndarray::ViewRepr<&mut f64>, Dim<[usize; 1]>> = (*dump).column_mut(i);
//         let mut min = col_i.to_owned();
//         Zip::from(&mut min).and(&ss).for_each(|z, &y| {*z = z.min(y)});

//         col_i -= &min;
//         min *= sp_price[i];
//         cost[i] += min.sum();
//         s -= &min;
//     };

//     *dump *= &od_price;
//     let unused_sp = s.sum() / usage.ncols() as f64;

//     cost + dump.sum_axis(Axis(0)) + unused_sp
// }
