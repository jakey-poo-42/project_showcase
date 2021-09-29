//
//  ViewController.swift
//  Business Card Printer
//
//  Created by Jacob McGee on 8/20/18.
//  Copyright © 2018 Jakey-Poo Builds Apps. All rights reserved.
//

import UIKit
import CoreData

class mainViewController: UIViewController, UINavigationControllerDelegate, UIImagePickerControllerDelegate {
    
    let viewBackground = UIImageView(image: nil)
    let businessCardViewer = UIImageView(frame: CGRect(x: 0, y: 0, width: 250, height: 400))
    var viewCenter = CGPoint()
    let fileManager = FileManager.default
    var imageLocation = 0
    
    // These are unneeded unless you include the functions in the "Unused Code" part
     let appDelegate = UIApplication.shared.delegate as! AppDelegate
/*
     let save = UserDefaults.standard
 */
    
    
    @IBAction func pickBackground(_ sender: Any) {
        imageLocation = 1
        let actionSheet = UIAlertController(title: nil, message: nil, preferredStyle: .actionSheet)
        
        actionSheet.addAction(UIAlertAction(title: "Use Photo from Camera", style: .default, handler: { (alert:UIAlertAction!) -> Void in self.camera()}))
        actionSheet.addAction(UIAlertAction(title: "Select Background from Library", style: .default, handler: { (alert:UIAlertAction!) -> Void in self.photoLibrary()}))
        actionSheet.addAction(UIAlertAction(title: "Choose Solid Background Color", style: .default, handler:
            { (alert:UIAlertAction!) -> Void in self.chooseSolidColor()}))
        actionSheet.addAction(UIAlertAction(title: "Remove Current Background", style:.destructive, handler:
            { (alert:UIAlertAction!) -> Void in self.removeBackground()}))
        actionSheet.addAction(UIAlertAction(title: "Cancel", style: .cancel, handler: nil))
        
        present(actionSheet, animated: true, completion: nil)
    }
    
    @IBOutlet var panController: UIPanGestureRecognizer!
    
    @IBAction func pan(_ sender: UIPanGestureRecognizer) {
        if (businessCardViewer.image == nil){
            print("No image selected. Aborting.")
            return
        }
        guard sender.view != nil else {
            print("No gesture recognizer found. Aborting.")
            return
        }
        
        let piece = sender.view!
        let translation = sender.translation(in: piece.superview)
        let maxXBuffer = view.bounds.maxX - 50
        let maxYBuffer = view.bounds.maxY - 50
        let minXBuffer = view.bounds.minX + 50
        let minYBuffer = view.bounds.minY + 50
        if (sender.state == .began){
            self.viewCenter = piece.center
        }
        if (sender.state != .cancelled || sender.state != .ended){
            let newCenter = CGPoint(x: viewCenter.x + translation.x, y: viewCenter.y + translation.y)
            businessCardViewer.center = newCenter
        } else {
            viewCenter = businessCardViewer.center
        }
        if (sender.state == .ended){
            print("Pan has ended.")
            print("Center coordinates: ", businessCardViewer.center.x, businessCardViewer.center.y)
            if (businessCardViewer.center.x >= maxXBuffer || businessCardViewer.center.y >= maxYBuffer || businessCardViewer.center.x <= minXBuffer || businessCardViewer.center.y <= minYBuffer){
                print("View out of bounds. Hiding.")
                businessCardViewer.isHidden = true
            }
        }
        
    }
    
    @IBAction func choosePictureButton(_ sender: Any) {
        imageLocation = 0
        let actionSheet = UIAlertController(title: nil, message: nil, preferredStyle: .actionSheet)
        
        actionSheet.addAction(UIAlertAction(title: "Take Photo", style: .default, handler: { (alert:UIAlertAction!) -> Void in self.camera()}))
        actionSheet.addAction(UIAlertAction(title: "Select Photo from Library", style: .default, handler: { (alert:UIAlertAction!) -> Void in self.photoLibrary()}))
        actionSheet.addAction(UIAlertAction(title: "Cancel", style: .cancel, handler: nil))
        
        present(actionSheet, animated: true, completion: nil)
    }
    
    @IBAction func printNewCard(_ sender: Any) {
        businessCardViewer.isHidden = false
        businessCardViewer.center = view.center
    }
    
    func camera() {
        let vc = UIImagePickerController()
        vc.sourceType = .camera
        vc.allowsEditing = false
        vc.delegate = self
        present(vc, animated: true)
    }
    
    func photoLibrary() {
        let vc = UIImagePickerController()
        vc.sourceType = .photoLibrary
        vc.allowsEditing = false
        vc.delegate = self
        present(vc, animated: true)
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
        picker.dismiss(animated: true)
        
        if let image = info[UIImagePickerControllerEditedImage] as? UIImage{
            print("Cropped image used.")
            if(imageLocation == 0){
                businessCardViewer.image = image
                saveImage(image: image, fileName: "cardFace")
            } else if(imageLocation == 1){
                viewBackground.image = image
                saveImage(image: image, fileName: "background")
            }
        } else if let image = info[UIImagePickerControllerOriginalImage] as? UIImage{
            print("Original image used.")
            if(imageLocation == 0){
                businessCardViewer.image = image
                saveImage(image: image, fileName: "cardFace")
            } else if(imageLocation == 1){
                viewBackground.image = image
                saveImage(image: image, fileName: "background")
            }
        } else {
            print("No image found.")
            return
        }
        if (businessCardViewer.isHidden){
            businessCardViewer.isHidden = false
        }
        
        businessCardViewer.center = view.center
    }
    
    func chooseSolidColor() {
        
        let colorPicker = UIAlertController(title: nil, message: nil, preferredStyle: .actionSheet)
        
        colorPicker.addAction(UIAlertAction(title: "Red", style: .default, handler: { (alert:UIAlertAction!) -> Void in self.red()}))
        colorPicker.addAction(UIAlertAction(title: "Orange", style: .default, handler: { (alert:UIAlertAction!) -> Void in self.orange()}))
        colorPicker.addAction(UIAlertAction(title: "Yellow", style: .default, handler: { (alert:UIAlertAction!) -> Void in self.yellow()}))
        colorPicker.addAction(UIAlertAction(title: "Green", style: .default, handler: { (alert:UIAlertAction!) -> Void in self.green()}))
        colorPicker.addAction(UIAlertAction(title: "Blue", style: .default, handler: { (alert:UIAlertAction!) -> Void in self.blue()}))
        colorPicker.addAction(UIAlertAction(title: "Cyan", style: .default, handler: { (alert:UIAlertAction!) -> Void in self.cyan()}))
        colorPicker.addAction(UIAlertAction(title: "Purple", style: .default, handler: { (alert:UIAlertAction!) -> Void in self.purple()}))
        colorPicker.addAction(UIAlertAction(title: "Black", style: .default, handler: { (alert:UIAlertAction!) -> Void in self.black()}))
        colorPicker.addAction(UIAlertAction(title: "Gray", style: .default, handler: { (alert:UIAlertAction!) -> Void in self.gray()}))
        colorPicker.addAction(UIAlertAction(title: "Cancel", style: .cancel, handler: nil))
        
        present(colorPicker, animated: true, completion: nil)
        
        if viewBackground.image != nil {
            viewBackground.image = nil
            deleteImage(fileName: "background")
        }
    }
    
    func removeBackground(){
        viewBackground.image = nil
        deleteImage(fileName: "background")
//        saveImage(image: viewBackground.image!, fileName: "background")
        view.backgroundColor = UIColor.white
    }
    
    func red(){
        view.backgroundColor = UIColor.red
    }
    func orange(){
        view.backgroundColor = UIColor.orange
    }
    func yellow(){
        view.backgroundColor = UIColor.yellow
    }
    func green(){
        view.backgroundColor = UIColor.green
    }
    func blue(){
        view.backgroundColor = UIColor.blue
    }
    func cyan(){
        view.backgroundColor = UIColor.cyan
    }
    func purple(){
        view.backgroundColor = UIColor.purple
    }
    func black(){
        view.backgroundColor = UIColor.black
    }
    func gray(){
        view.backgroundColor = UIColor.gray
    }
    
    func saveImage(image: UIImage, fileName: String){
        guard let data = UIImagePNGRepresentation(image) else{
            return
        }
        guard let directory = try? fileManager.url(for: .documentDirectory, in: .userDomainMask, appropriateFor: nil, create: false) as NSURL else {
            return
        }
        
        do {
            try data.write(to: directory.appendingPathComponent("\(fileName).png")!)
        } catch {
            print("Error saving: \(error.localizedDescription)")
            return
        }
    }
    
    func loadImage(fileName: String) -> UIImage?{
        if let dir = try? FileManager.default.url(for: .documentDirectory, in: .userDomainMask, appropriateFor: nil, create: false) {
            return UIImage(contentsOfFile: URL(fileURLWithPath: dir.absoluteString).appendingPathComponent(fileName).path)
        }
        return nil
    }
    
    func deleteImage(fileName: String) {
        guard let directory = try? fileManager.url(for: .documentDirectory, in: .userDomainMask, appropriateFor: nil, create: false) as NSURL else {
            return
        }
        try? fileManager.removeItem(at: directory.appendingPathComponent("\(fileName).png")!)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        view.addSubview(businessCardViewer)
        view.addSubview(viewBackground)
        view.sendSubview(toBack: viewBackground)
        businessCardViewer.isUserInteractionEnabled = true
        view.isUserInteractionEnabled = true
        viewBackground.isUserInteractionEnabled = false
        businessCardViewer.center = view.center
        viewBackground.center = view.center
        businessCardViewer.contentMode = .scaleAspectFill
        viewBackground.contentMode = .scaleToFill
        viewBackground.bounds = CGRect(origin: view.center, size: CGSize(width: view.bounds.maxX, height: view.bounds.maxY))
        panController.minimumNumberOfTouches = 1
        businessCardViewer.addGestureRecognizer(panController)
        print("View bounds: Min(", view.bounds.minX, view.bounds.minY, ") Max(", view.bounds.maxX, view.bounds.maxY, ")")
        print("Hide/don't hide buffer coordinates: Min(", view.bounds.minX + 50, view.bounds.minY + 50, ") Max(", view.bounds.maxX - 50, view.bounds.maxY - 50, ")")
        businessCardViewer.bounds = CGRect(origin: view.center, size: CGSize(width: 250, height: 400))
        
        if let cardFaceImage = loadImage(fileName: "cardFace.png"){
            businessCardViewer.image = cardFaceImage
        }
        if let backgroundImage = loadImage(fileName: "background.png"){
            viewBackground.image = backgroundImage
        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func viewDidAppear(_ animated: Bool) {
        // Instead of fucking with Core Data, I decided to place a text file on the user's device. The text file will contain the password if the user has put in the correct password and "badKey" otherwise. Core Data was causing too many problems to just check one god damn bool value, so I did this instead
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let accessCodeView = storyboard.instantiateViewController(withIdentifier: "accessCodeViewController")
        
        let accessKey = "accessKey.txt"
        let badKey = "badKey"
        let key = "15$3c0nd$"
        
        if let documentsURL = fileManager.urls(for: .documentDirectory, in: .userDomainMask).first {
//            let documentPath = documentsURL.path
            let filePath = documentsURL.appendingPathComponent(accessKey)
            print("Access Key file is at", filePath)
            
            do {
//              let files = try fileManager.contentsOfDirectory(atPath: "\(documentPath)")
//                print("File exists?",fileManager.fileExists(atPath: "\(filePath)"))
//                if (fileManager.fileExists(atPath: "\(filePath)") ==  false){
//                    try badKey.write(to: filePath, atomically: true, encoding: .utf8)
//                }
                let input = try String(contentsOf: filePath, encoding: .utf8)
                print("Saved string: \(input)")
                print("Expected string: \(key)")
                if (input != key){
                    print("Keys do not match.")
                    present(accessCodeView, animated: true, completion: nil)
                }
            } catch {
                print("Error thrown in do block of viewDidAppear: \(error)")
                print("Attempting to create file...")
                do {
                    try badKey.write(to: filePath, atomically: true, encoding: .utf8)
                    print("File created successfully")
                    present(accessCodeView, animated:true, completion: nil)
                } catch {
                    print("Error creating file: \(error)")
                }
                
            }
        }
    }
}


// MARK: Unused code that might come in handy later
/*
 // Was in imagePickerController()
        save.set(userImage, forKey: "CardFace")

        if (save.object(forKey: "CardFace") != nil) {
            print("Card saved successfully.")
        } else {
            print("There was an error saving the card face.")
        }
        let documentsURL = fileManager.urls(for: .documentDirectory, in: .userDomainMask).first!
        let documentsPath = documentsURL.path
        let filePath = documentsURL.appendingPathComponent("cardFace.png")

        do {
            let files = try fileManager.contentsOfDirectory(atPath: "\(documentsPath)")

            for file in files{
                // Check to make sure saved data doesn't already exist
                if ("\(documentsPath)/\(file)" == filePath.path){
                    try fileManager.removeItem(atPath: filePath.path)
                }
            }
        } catch {
            print("Could not add image from document directory: \(error)")
        }

        do {
            if let pngImageData =  UIImagePNGRepresentation((businessCardViewer.image)!) {
                try pngImageData.write(to: filePath, options: .atomic)
            }
        } catch {
            print("Failed to save image: \(error)")
        }

        let container = appDelegate.persistentContainer
        let context = container.viewContext
 
 // Was in viewDidLoad()
         if(save.object(forKey: "CardFace") != nil){
             businessCardViewer.image = save.object(forKey: "CardFace") as? UIImage
         } else {
             print("User has not set card image or there was an error saving the card image.")
         }
 
         if (save.object(forKey: "Background") != nil) {
             viewBackground.image = save.object(forKey: "Background") as? UIImage
         } else {
             print("User has not set background or there was an error saving the background.")
         }
 
     func fetchData() {
         let container = appDelegate.persistentContainer
         let context = container.viewContext
         let fetchRequest = NSFetchRequest<Image>(entityName: "Image")
     }
 
 //            let result = try context.fetch(request)
 //            for data in result as! [NSManagedObject]{
 //                print(data.value(forKeyPath: "passwordCorrect"))
 //                if (data.value(forKeyPath: "passwordCorrect") == nil){
 //                    print("No previous data found. Creating new data.")
 //                    passwordCorrect.setValue(false, forKeyPath: "passwordCorrect")
 //                    do {
 //                        try context.save()
 //                    } catch {
 //                        print("Error saving initial value: \(error)")
 //                    }
 //                    print("Access Granted? >", data.value(forKey: "passwordCorrect") as! Bool)
 //                } else {
 //                    print("Access Granted? >", data.value(forKey: "passwordCorrect") as! Bool)
 //                }
 //                if (data.value(forKeyPath: "passwordCorrect") as! Bool != true) {
 //                    let alert = UIAlertController(title: "Enter Access Code", message: nil, preferredStyle: .alert)
 //
 //                    alert.addTextField { (textField) in
 //                    }
 //
 //                    alert.addAction(UIAlertAction(title: "Submit", style: .default, handler: { [weak alert] (_) in
 //                        let textField = alert!.textFields![0]
 //                        if textField.text == "password" {
 //                            self.dismiss(animated: true, completion: nil)
 //                            passwordCorrect.setValue(true, forKeyPath: "passwordCorrect")
 //                            do {
 //                                try context.save()
 //                            } catch {
 //                                print("Error saving: \(error)")
 //                            }
 //                        } else {
 //
 //                        }
 //                    }))
 //
 //                    present(alert, animated: true, completion: nil)
 ////                    present(accessCodeView, animated: true, completion: nil)
 //                    break
 //                 } else {
 //                   break
 }
 
 
 let container = appDelegate.persistentContainer
 let context = container.viewContext
 let entity = NSEntityDescription.entity(forEntityName: "Password", in: context)
 let passwordCorrect = NSManagedObject(entity: entity!, insertInto: context)
 
 let storyboard = UIStoryboard(name: "Main", bundle: nil)
 let accessCodeView = storyboard.instantiateViewController(withIdentifier: "accessCodeViewController")
 
 let request = NSFetchRequest<NSFetchRequestResult>(entityName: "Password")
 request.returnsObjectsAsFaults = false
 request.fetchLimit = 1
 
 do {
 let result = try context.fetch(request)
 for data in result as! [NSManagedObject] {
 print("\n\nResult 1:\n\n")
 print(data)
 print(data.value(forKey: "passwordCorrect"))
 }
 
 passwordCorrect.setValue(false, forKey: "passwordCorrect")
 
 try context.save()
 
 let newResult = try context.fetch(request)
 for data in newResult as! [NSManagedObject]{
 print("\n\nResult 2:\n\n")
 print(data)
 print(data.value(forKey: "passwordCorrect"))
 }
 
 } catch {
 print("Error fetching data: \(error)")
 }
*/
