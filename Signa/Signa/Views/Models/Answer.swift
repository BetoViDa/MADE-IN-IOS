//
//  Answer.swift
//  triviapi
//
//  Created by Victoria Lucero on 10/11/22.
//

import Foundation

struct Answer: Identifiable{
    var id = UUID()
    var text : AttributedString
    var isCorrect:Bool
}
