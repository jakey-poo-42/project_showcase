//
//  aboutViewController.swift
//  Business Card Printer
//
//  Created by Jacob McGee on 8/22/18.
//  Copyright © 2018 Jakey-Poo Builds Apps. All rights reserved.
//

import Foundation
import UIKit

//TODO: (Storyboard) Add copyright information
//TODO: (Storyboard) Combine credits into a stack and create constraints for the stack

class aboutViewController: UIViewController {
    @IBAction func dismissAbout(_ sender: Any) {
        dismiss(animated: true, completion: nil)
    }
    @IBAction func openWebsite(_ sender: Any) {
        UIApplication.shared.open(URL(string: "https://www.christophejelinski.com")!)
    }
    
    @IBAction func openEmail(_ sender: Any) {
        UIApplication.shared.open(URL(string: "mailto:jmcgee2019@gmail.com")!)
    }
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
}
