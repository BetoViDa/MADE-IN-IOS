//
//  loginswiftApp.swift
//  loginswift
//
//  Created by Macías Romero on 09/11/22.
//

import SwiftUI

@main
struct loginswiftApp: App {
    let persistenceController = PersistenceController.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, persistenceController.container.viewContext)
        }
    }
}
