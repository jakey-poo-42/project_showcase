//
//  accessCodeViewController.swift
//  Business Card Printer
//
//  Created by Jacob McGee on 9/7/18.
//  Copyright © 2018 Jakey-Poo Builds Apps. All rights reserved.
//

import Foundation
import UIKit
import CoreData

class accessCodeViewController: UIViewController{
    let fileManager = FileManager.default
    let appDelegate = UIApplication.shared.delegate as! AppDelegate
    
    @IBOutlet weak var codeField: UITextField!
    
    @IBAction func submitCode(_ sender: Any) {
        let accessKey = "accessKey.txt"
        
        let key = codeField.text
        if let directory = fileManager.urls(for: .documentDirectory, in: .userDomainMask).first {
            let fileURL = directory.appendingPathComponent(accessKey)
            print("Access Key file is at ", fileURL)
            
            if (key == "15$3c0nd$") {
                do {
                    try key?.write(to: fileURL, atomically: false, encoding: .utf8)
                } catch {
                    print("Error writing to file: \(error)")
                }
                
                dismiss(animated: true, completion: nil)
            } else {
                let alert = UIAlertController(title: "Incorrect access code.", message: nil, preferredStyle: .alert)
                alert.addAction(UIAlertAction(title: "Dismiss", style: .default, handler: nil))
                
                present(alert, animated: true, completion: nil)
            }
        }
    }
    
//    func fetchData(){
//        let container = appDelegate.persistentContainer
//        let context = container.viewContext
//    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
}
