//
//  TriviaView.swift
//  triviapi
//
//  Created by Victoria Lucero on 11/11/22.
//

import SwiftUI

struct TriviaView: View {
    @EnvironmentObject var triviaManager: TriviaManager

    var body: some View {
        if triviaManager.reachedEnd{
            VStack(spacing: 20){
                title(text:"Trivia game")
                Text("Felicidades terminaste el quizz!")
                Text("You scored \(triviaManager.score) out of \(triviaManager.length)")
                Button{
                    Task.init{
                        await triviaManager.fetchTrivia()
                    }
                } label: {
                    PrimaryButtom(text: "Play again")
                }
            }.foregroundColor(Color("AccentColor"))
                .padding()
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .background(.white)
        }else{
            QuestionView()
                .environmentObject(triviaManager)
        }
       
    }
}

struct TriviaView_Previews: PreviewProvider {
    static var previews: some View {
        TriviaView()
            .environmentObject(TriviaManager())
    }
}
