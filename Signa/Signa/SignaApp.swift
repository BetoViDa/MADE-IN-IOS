//
//  SignaApp.swift
//  Signa
//
//  Created by Macías Romero on 10/11/22.
//

import SwiftUI

@main
struct SignaApp: App {
    let persistenceController = PersistenceController.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, persistenceController.container.viewContext)
        }
    }
}
