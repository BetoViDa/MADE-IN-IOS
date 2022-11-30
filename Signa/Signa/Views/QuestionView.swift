//
//  QuestionView.swift
//  triviapi
//
//  Created by Victoria Lucero on 10/11/22.
//

import SwiftUI
import AVKit

struct QuestionView: View {
    @EnvironmentObject var triviaManager: TriviaManager
    
    var body: some View {
        
            VStack(spacing: 40){
                HStack{
                    title(text: "\(TriviaCategor)")
                        .padding(.horizontal)
                    Spacer()
                    Text("\(triviaManager.index + 1) de \(triviaManager.length)")
                        .foregroundColor(Color("AccentColor"))
                        .fontWeight(.heavy)
                        .padding(.horizontal)
                    
                }
                
                ProgressBar(progress: triviaManager.progress)
                
                //Spacer()
                ScrollView{
                VStack(alignment: .center, spacing: 20){
                    //if((triviaManager.trivia[triviaManager.index].answer) != nil) {
                        if(triviaManager.trivia[triviaManager.index].fileType){ // true = image
                            // mostramos una imagen
                            AsyncImage(url: URL(string: urlFiles + triviaManager.trivia[triviaManager.index].answer.lowercased() + ".JPG")){ phase in
                                switch phase {
                                case .success(let image):
                                    image.resizable().frame(width: 300, height: 200)
                                        .padding(.horizontal,2)
                                case .failure(let error):
                                    let _ = print(error)
                                    //Text("error: \(error.localizedDescription)")
                                    Text("error al cargar la imagen")
                                case .empty:
                                    ProgressView()
                                @unknown default:
                                    fatalError()
                                }
                            }
                            
                        } else {
                            // mostramos un video
                            let strpalabra : String = triviaManager.trivia[triviaManager.index].answer.replacingOccurrences(of: " ", with: "%20")
                            VideoPlayer(player: AVPlayer(url: URL(string: urlFiles + strpalabra + "_Web.m4v")!))
                                .frame(width: 300, height: 200)
                                .padding(.horizontal)
                        }
                    //}
                    
                    ForEach(triviaManager.answerChoices, id: \.id){
                        answer in AnswerRow(answer:answer)
                            .environmentObject(triviaManager)
                    }.padding(.horizontal)
                    
                }
                
                Button{
                    triviaManager.goToNextQuestion()
                } label:{
                    PrimaryButtom(text: "Siguiente", background: triviaManager.answerSelected ?  Color("AccentColor") : Color("adb5bd") ).foregroundColor(Color(.white))
                }
                .disabled(!triviaManager.answerSelected)
                
            }.frame(maxWidth: .infinity, maxHeight: .infinity)
        }
    }
    
    struct QuestionView_Previews: PreviewProvider {
        static var previews: some View {
            QuestionView()
                .environmentObject(TriviaManager())
        }
    }
}
