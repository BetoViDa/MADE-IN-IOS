//
//  AdminView.swift
//  Signa
//
//  Created by Victoria Lucero on 15/11/22.
//

import SwiftUI

struct AdminView: View {
    //downloading amounts
    @State private var downloadAmount = 0.0
    @State private var downloadAmount2 = 0.0
    @State private var downloadAmount3 = 0.0
    @State private var downloadAmount4 = 0.0
    @State private var downloadAmount5 = 0.0
    //current progress
    @State var progress = 90.0//
    @State var progress2 = 54.0//
    @State var progress3 = 36.0//
    @State var progress4 = 99.0//
    @State var progress5 = 23.0//
    
    //timers
    let timer = Timer.publish(every: 0.1, on: .main, in: .common).autoconnect()
    let timer2 = Timer.publish(every: 0.1, on: .main, in: .common).autoconnect()
    let timer3 = Timer.publish(every: 0.1, on: .main, in: .common).autoconnect()
    let timer4 = Timer.publish(every: 0.1, on: .main, in: .common).autoconnect()
    let timer5 = Timer.publish(every: 0.1, on: .main, in: .common).autoconnect()
    let lightPurple = Color(red: 156/255, green: 16/255, blue: 179/255)
    let darkPurple = Color(red: 11/255, green: 13/255, blue: 50/255)
    let signa = Color(red: 48/256, green: 212/256, blue: 200/256)

    var body: some View {
        NavigationView {
                ScrollView {
                        VStack {
                    
                            
                            HStack {
                                ProgressView("", value: downloadAmount, total: 100)
                                    .accentColor(signa)
                                    .scaleEffect(x: 0.8, y: 8, anchor: .center)
                                    .padding()
                            }
                            
                            ProgressView("", value: downloadAmount2, total: 100)
                                .accentColor(signa)
                                .scaleEffect(x: 0.8, y: 8, anchor: .center)
                                .padding()
                            ProgressView("", value: downloadAmount3, total: 100)
                                .accentColor(signa)
                                .scaleEffect(x: 0.8, y: 8, anchor: .center)
                                .padding()
                            
                            ProgressView("", value: downloadAmount4, total: 100)
                                .accentColor(signa)
                                .scaleEffect(x: 0.8, y: 8, anchor: .center)
                                .padding()
                            
                            ProgressView("", value: downloadAmount5, total: 100)
                                .accentColor(signa)
                                .scaleEffect(x: 0.8, y: 8, anchor: .center)
                                .padding()
                            
                            
                        }
                        
                
                .onReceive(timer) { _ in
                    //sustituir este valor
                    if downloadAmount >= progress {
                        self.timer.upstream.connect().cancel()
                    }
                    
                    if downloadAmount < 100 {
                        downloadAmount += Double.random(in: 2...4)
                    }
                    
                }
                
                .onReceive(timer2) { _ in
                    
                    
                    
                    if downloadAmount2 >= progress2 {
                        self.timer2.upstream.connect().cancel()
                    }
                    
                    if downloadAmount2 < 100 {
                        downloadAmount2 += Double.random(in: 2...4)
                    }
                }
                .onReceive(timer3) { _ in
                    
                    if downloadAmount3 >= progress3 {
                        self.timer3.upstream.connect().cancel()
                    }
                    
                    if downloadAmount3 < 100 {
                        downloadAmount3 += Double.random(in: 2...4)
                    }
                }
                
                .onReceive(timer4) { _ in
                    
                    if downloadAmount4 >= progress4 {
                        self.timer4.upstream.connect().cancel()
                    }
                    
                    if downloadAmount4 < 100 {
                        downloadAmount4 += Double.random(in: 2...4)
                    }
                }
                .onReceive(timer5) { _ in
                    
                    if downloadAmount5 >= progress5 {
                        self.timer5.upstream.connect().cancel()
                    }
                    
                    if downloadAmount5 < 100 {
                        downloadAmount5 += Double.random(in: 2...4)
                    }
                }
                
            }
            
        }
    }
}

struct AdminView_Previews: PreviewProvider {
    static var previews: some View {
        AdminView()
    }
}
