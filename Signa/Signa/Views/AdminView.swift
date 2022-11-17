//
//  AdminView.swift
//  Signa
//
//  Created by Victoria Lucero on 15/11/22.
//

import SwiftUI
import WrappingHStack

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
    
    
    var topicsSize : [Font] = [.title2,.title2,.title3,.system(size: 19)]
    
    struct DataProgress : Codable {
        var name : [String]
        var percentage : [Int]
    }
    
    @State var name : String = ""
    @State var percentage : Int = 0
    @State var results : DataProgress?
    
    //timers
    let timer = Timer.publish(every: 0.1, on: .main, in: .common).autoconnect()
    /*
     let timer2 = Timer.publish(every: 0.1, on: .main, in: .common).autoconnect()
     let timer3 = Timer.publish(every: 0.1, on: .main, in: .common).autoconnect()
     let timer4 = Timer.publish(every: 0.1, on: .main, in: .common).autoconnect()
     let timer5 = Timer.publish(every: 0.1, on: .main, in: .common).autoconnect()
     */
    let signa = Color(red: 48/256, green: 212/256, blue: 200/256)
    
    func loadData(){
        guard let url = URL(string: "http://127.0.0.1:5000/group/\(logedUser.group)") else {
            print("Invalid URL")
            return
        }
        let request = URLRequest(url: url)
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let data = data {
                if let response = try? JSONDecoder().decode(DataProgress.self, from: data) {
                    DispatchQueue.main.async {
                        self.results = response
                    }
                    return
                }
            }
        }.resume()
    }
    
    
    var body: some View {
        NavigationView {
            ScrollView {
                
                Group {
                    /*
                     HStack{
                     Text("Tópicos")
                     .font(.title)
                     .fontWeight(.bold)
                     .multilineTextAlignment(.center).padding()
                     Spacer()
                     }
                     */
                    
                    
                    VStack {
                        
                        ForEach((0...20), id: \.self){index in
                            VStack(alignment: .center){
                                Button(action: {
                                    downloadAmount = downloadAmount[index]
                                    loadData()
                                    
                                }){
                                    ProgressView("", value: downloadAmount, total: 100)
                                        .accentColor(signa)
                                        .scaleEffect(x: 0.8, y: 8, anchor: .center)
                                        .padding()
                                    
                                }
                            }
                        }
                        /*
                         ProgressView("", value: downloadAmount, total: 100)
                         .accentColor(signa)
                         .scaleEffect(x: 0.8, y: 8, anchor: .center)
                         .padding()
                         
                         
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
                         
                         */
                    }
                    
                    
                    Group {
                        VStack {
                            Image("karate")
                                .scaleEffect(0.5)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7)
                            VStack{
                                Text("Da Admin")
                                    .font(.title)
                                    .fontWeight(.bold)
                                
                                HStack {
                                    Text("Nivel 1")
                                        .font(.subheadline)
                                    Spacer()
                                }
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                                
                                Divider()
                                VStack(alignment: .leading){
                                    
                                    HStack(alignment: .top) {
                                        Text("Description")
                                            .font(.title2)
                                            .fontWeight(.semibold)
                                        Spacer()
                                    }
                                    Text("Descriptive text goes here.")
                                        .foregroundColor(.secondary)
                                    
                                }
                            }
                            .padding()
                        }
                    }
                    
                    .onReceive(timer) { _ in
                        //sustituir este valor
                        if downloadAmount[index] >= percentage[index] {
                            self.timer.upstream.connect().cancel()
                        }
                        
                        if downloadAmount[index] < 100 {
                            downloadAmount[index] += Double.random(in: 2...4)
                        }
                        
                    }
                    /*
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
                     */
                    
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
