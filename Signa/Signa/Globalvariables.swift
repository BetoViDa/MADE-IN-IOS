//
//  Globalvariables.swift
//  loginswift
//
//  Created by Victoria Lucero on 09/11/22.
//

import SwiftUI

public struct User: Codable{
    var _id : String
    var username : String
    var email : String
    var type : Int // 1 es admin, 0 es normal
    var group : String
    var lvl : Int
}

public var logedUser = User(
    _id : "",
    username : "",
    email : "",
    type : 0,
    group : "",
    lvl : 0
)

//public let UrlDriveFiles = "https://drive.google.com/uc?export=view&id="
public let urlFiles = "http://198.37.117.228:5434/multimedia/"
public let APIURL: String = "http://198.37.117.228:5433"
public var TriviaCategor: String = ""   //Variable para el Quiz
