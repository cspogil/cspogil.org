' removeAnswers()
' Copyright (c) 2022 Politechnika Lodzka (Lodz University of Technology)
' This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
' Developed by Laurent Babout (laurent.babout@p.lodz.pl) and Clif Kussmaul (clif@kussmaul.org).

Sub removeAnswers()
    Dim i     As Long
    Dim rng   As Range
    Dim c     As Cell
    Dim p     As Paragraph
    Dim o     As OMath
    Dim fName As String
    Dim fPath As String
    Dim nName As String

    fPath = ActiveDocument.Path ' location on disc
    oName = ActiveDocument.Name ' (old) filename
    nName = Mid(oName, 1, InStr(1, oName, ".doc") - 1) & "-student.docx"
    ActiveDocument.SaveAs2 (fPath & "/" & nName) ' save as new file for student instructions

    Set rng = ActiveDocument.Range        ' range object that contains all the text of the current active document (where the cursor is)

    For Each o In rng.OMaths              ' first look at all equations in the file
        If o.Range.Style = "Answer" Then  ' check their style and remove as needed
            o.Range.Style = wdStyleNormal
            o.Range.Delete
        End If
    Next
    'For Each p In rng.Paragraphs             ' then look at paragraphs
    For i = rng.Paragraphs.Count To 1 Step -1 ' loop backwards to avoid problems
        Set p = rng.Paragraphs(i)
        If p.Style = "Answer" Then            ' check their style and remove as needed
            'p.Range.Delete
            p.Style = wdStyleNormal
            If p.Range.Tables.Count > 0 Then
                p.Range.Text = ""
            Else
                p.Range.Text = vbCrLf
            End If
        End If
    Next

    ActiveDocument.Save
End Sub
