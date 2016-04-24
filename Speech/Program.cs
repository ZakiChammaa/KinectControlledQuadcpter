using System;
using System.IO;
using System.Linq;
using Microsoft.Research.Kinect.Audio;
using Microsoft.Speech.AudioFormat;
using Microsoft.Speech.Recognition;

namespace Speech
{
    class Program
    {
        static void Main()
        {
            using (var source = new KinectAudioSource())
            {
                source.FeatureMode = true;
                source.AutomaticGainControl = false;
                source.SystemMode = SystemMode.OptibeamArrayOnly;

                RecognizerInfo ri = GetKinectRecognizer();

                if (ri == null)
                {
                    Console.WriteLine("Could not find Kinect speech recognizer. Please refer to the sample requirements.");
                    return;
                }

                Console.WriteLine("Using: {0}", ri.Name);

                using (var sre = new SpeechRecognitionEngine(ri.Id))
                {
                    //declare commands to be used
                    var commands = new Choices();
                    commands.Add("activate");
                    commands.Add("off");
                    commands.Add("open");
                    commands.Add("manual");
                    commands.Add("hold");
                    commands.Add("land");
                    commands.Add("stabilize");

                    var gb = new GrammarBuilder {Culture = ri.Culture};
                    //Specify the culture to match the recognizer in case we are running in a different culture.                                 
                    gb.Append(commands);

                    // Create the actual Grammar instance, and then load it into the speech recognizer.
                    var g = new Grammar(gb);

                    sre.LoadGrammar(g);
                    sre.SpeechRecognized += SreSpeechRecognized;
                    sre.SpeechRecognitionRejected += SreSpeechRejected;

                    using (Stream s = source.Start())
                    {
                        sre.SetInputToAudioStream(s,
                                                  new SpeechAudioFormatInfo(
                                                      EncodingFormat.Pcm, 16000, 16, 1,
                                                      32000, 2, null));

                        Console.WriteLine("Recognizing... Press ENTER to stop");

                        sre.RecognizeAsync(RecognizeMode.Multiple);
                        Console.ReadLine();
                        Console.WriteLine("Stopping recognizer ...");
                        sre.RecognizeAsyncStop();
                    }
                }
            }
        }

        private static RecognizerInfo GetKinectRecognizer()
        {
            Func<RecognizerInfo, bool> matchingFunc = r =>
            {
                string value;
                r.AdditionalInfo.TryGetValue("Kinect", out value);
                return "True".Equals(value, StringComparison.InvariantCultureIgnoreCase) && "en-US".Equals(r.Culture.Name, StringComparison.InvariantCultureIgnoreCase);
            };
            return SpeechRecognitionEngine.InstalledRecognizers().Where(matchingFunc).FirstOrDefault();
        }

        static void SreSpeechRejected(object sender, SpeechRecognitionRejectedEventArgs e)
        {
			Console.WriteLine("\nSpeech Rejected");
        }

        static void SreSpeechRecognized(object sender, SpeechRecognizedEventArgs e)
        {
            Console.WriteLine("\nSpeech Recognized:{0}", e.Result.Text);
        }
    }
}