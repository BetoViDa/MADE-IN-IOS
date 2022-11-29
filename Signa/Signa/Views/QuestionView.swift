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
        ScrollView{
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
                VStack(alignment: .leading, spacing: 20){
                    
                    if(triviaManager.trivia[triviaManager.index].fileType){ // true = image
                        // mostramos una imagen
                        AsyncImage(url: URL(string: UrlDriveFiles + triviaManager.trivia[triviaManager.index].file)){ image in
                            image.resizable().frame(width: 350, height: 230)
                                .padding(.horizontal)
                        } placeholder: {
                            ProgressView()
                        }
                        
                    } else {
                        // mostramos un video
                        VideoPlayer(player: AVPlayer(url: URL(string: UrlDriveFiles + triviaManager.trivia[triviaManager.index].file)!))
                            .frame(width: 350, height: 230)
                            .padding(.horizontal)
                    }
                    
                    ForEach(triviaManager.answerChoices, id: \.id){
                        answer in AnswerRow(answer:answer)
                            .environmentObject(triviaManager)
                    }.padding(.horizontal)
                    
                }
                
                Button{
                    triviaManager.goToNextQuestion()
                } label:{
                    PrimaryButtom(text: "Siguiente", background: triviaManager.answerSelected ?  Color("AccentColor") : Color("adb5bd") )
                }
                .disabled(!triviaManager.answerSelected)
                
            }.padding()
                .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
    }
    
    struct QuestionView_Previews: PreviewProvider {
        static var previews: some View {
            QuestionView()
                .environmentObject(TriviaManager())
        }
    }
}
