import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import Message from "@/components/ui/message";

export default function Home() {
  return (
    <div className=" text-white p-3 w-full flex flex-col">
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Chat</CardTitle>
          <CardDescription>Conversation between users</CardDescription>
        </CardHeader>
        <CardContent>
          <Message
            avatar="https://icons.iconarchive.com/icons/iconarchive/robot-avatar/256/Orange-1-Robot-Avatar-icon.png"
            name="AI-1"
            message="Hello, how are you?"
            isSender={false}
          />
          <Message
            avatar="https://icons.iconarchive.com/icons/iconarchive/robot-avatar/256/Orange-1-Robot-Avatar-icon.png"
            name="AI-2"
            message="I'm good, thanks! How about you?"
            isSender={true}
          />
        </CardContent>
        <CardFooter className="flex flex-row items-center">
          <Textarea placeholder="Type your message here." className="flex-grow" />
          <Button className="ml-3">Send</Button>
        </CardFooter>
      </Card>
    </div>
  );
}