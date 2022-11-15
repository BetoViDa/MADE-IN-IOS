//
//  Extensions.swift
//  triviapi
//
//  Created by Victoria Lucero on 10/11/22.
//

import Foundation
import SwiftUI

struct title: View {
    var text: String
    var body: some View {
        Text(text)
            .font(.title)
            .fontWeight(.heavy)
            .foregroundColor(Color("AccentColor"))
    }
}

