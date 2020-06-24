(*
	Get images in Finder selection, then call the workflow again with
	the first selected image.

	If no images are selected, return an error message, which
	can be passed to a Post Notification action.
*)

-- The filetypes understood by Google Image Search
set imageExtensions to {"jpg", "jpeg", "bmp", "gif", "png"}

-- Return list of files selected in Finder whose extensions are
-- in imageExtensions
on selectedImages()
	set theImages to {}
	tell application "Finder"
		set theSelection to the selection
		if (the count of theSelection) is greater than 0 then
			repeat with theFile in theSelection
				if the name extension of theFile is in my imageExtensions then
					set the end of theImages to (theFile as alias)
				end if
			end repeat
		end if
		log ((the count of theImages) as text) & " image(s) selected"
	end tell
	return theImages
end selectedImages

set theImages to my selectedImages()
if (count of theImages) is greater than 0 then
	set theImage to item 1 of theImages
	set thePath to POSIX path of theImage

	-- Use the workflow's own external trigger
	tell application id "com.runningwithcrayons.Alfred" to run trigger "Find Similar Images" in workflow "net.deanishe.alfred-google-similar-images" with argument thePath
else
	return "No images selected"
end if
