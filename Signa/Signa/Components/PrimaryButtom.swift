//
//  PrimaryButtom.swift
//  triviapi
//
//  Created by Victoria Lucero on 10/11/22.
//

import SwiftUI

struct PrimaryButtom: View {
    var text: String
    var background: Color = Color("AccentColor")
    var body: some View {
        Text(text)
            .foregroundColor(.blue)
            .padding()
            .padding(.horizontal)
            .background(background)
            .cornerRadius(30)
            .shadow(radius: 10)
    }
}

struct PrimaryButtom_Previews: PreviewProvider {
    static var previews: some View {
        PrimaryButtom(text: "NEXT")
    }
}
