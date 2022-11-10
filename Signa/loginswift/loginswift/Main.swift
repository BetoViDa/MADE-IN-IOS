//
//  Main.swift
//  loginswift
//
//  Created by Victoria Lucero on 09/11/22.
//

import SwiftUI

public var PruebaGlobalVar: String = "hola"


struct Main: View {
    var body: some View {
        Text("MAIIIIN")
        Text(APIURL)
    }
}

struct Main_Previews: PreviewProvider {
    static var previews: some View {
        Main()
    }
}
