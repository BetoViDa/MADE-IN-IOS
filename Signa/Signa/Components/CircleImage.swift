//
//  CircleImage.swift
//  ToCombine
//
//  Created by Victoria Lucero on 12/11/22.
//

import SwiftUI

struct CircleImage: View {
    var body: some View {
        Image("earth3")
            .scaleEffect(0.18)
            .frame(width:100, height: 100)
            .scaledToFit()
            .clipShape(Circle())
            .overlay {
                Circle().stroke(.white, lineWidth: 4)
            }
            .shadow(radius: 7)
        
    }
}

struct CircleImage_Previews: PreviewProvider {
    static var previews: some View {
        CircleImage()
    }
}
