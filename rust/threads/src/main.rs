use std::thread;
use std::time::Duration;

fn main() {
    let v = vec![1, 2, 3];

    let handle = thread::spawn(move || {
        println!("Here's a vector: {:?}", v);
    });

    // can't drop v here, since it has already been moved into the closure
    // drop(v);
    handle.join().unwrap();
}

// fn main() {
//     let handle = thread::spawn(|| {
//         for i in 1..10 {
//             println!("hi number {} from the spawned thred!", i);
//             thread::sleep(Duration::from_millis(1));
//         }
//     });
//     // handle.join().unwrap();
// 
//     for i in 1..5 {
//         println!("hi number {} from the main thread!", i);
//         thread::sleep(Duration::from_millis(1));
//     }
// 
//     handle.join().unwrap();
// }
