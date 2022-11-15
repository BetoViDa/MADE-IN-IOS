//
//  ProgressBar.swift
//  triviapi
//
//  Created by Victoria Lucero on 10/11/22.
//

import SwiftUI

struct ProgressBar: View {
    var progress: CGFloat
    
    var body: some View {
        ZStack(alignment: .leading){
            Rectangle()
                .frame(maxWidth: 350, maxHeight: 4)
                .foregroundColor(Color("adb5bd"))
                .cornerRadius(10)
            Rectangle()
                .frame(width: progress,height: 4)
                .foregroundColor(Color("AccentColor"))
                .cornerRadius(10)
        }
    }
}

struct ProgressBar_Previews: PreviewProvider {
    static var previews: some View {
        ProgressBar(progress: 70)
    }
}
